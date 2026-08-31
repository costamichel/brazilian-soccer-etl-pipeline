import os
import requests
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# =============================================================================
# 0. CONFIGURAÇÃO DE AMBIENTE E BANCO DE DADOS
# =============================================================================
load_dotenv()
db_url = os.getenv("DATABASE_URL")

# Se a URL começar com 'postgres://', o SQLAlchemy moderno prefere 'postgresql://'
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

engine = create_engine(db_url)
print("☁️ Conectando ao Supabase...")

# =============================================================================
# FUNÇÕES DE LIMPEZA E TRATAMENTO
# =============================================================================
def extrair_url_escudo(escudos: dict) -> str:
    if isinstance(escudos, dict):
        return escudos.get('60x60')
    return None

def limpar_nome_time(linha: pd.Series) -> str:
    correcoes = {
        'atletico-mg': 'Atlético-MG', 'atletico-pr': 'Athletico-PR', 
        'atletico-go': 'Atlético-GO', 'sao-paulo': 'São Paulo',
        'gremio': 'Grêmio', 'corinthians': 'Corinthians',
        'vitoria': 'Vitória', 'goias': 'Goiás',
        'ceara': 'Ceará', 'cuiaba': 'Cuiabá',
        'avai': 'Avaí', 'parana': 'Paraná'
    }
    slug = linha.get('slug')
    nome_fantasia = str(linha.get('nome_fantasia'))
    
    if pd.notna(slug) and slug in correcoes:
        return correcoes[slug]
    if len(nome_fantasia) <= 3 and pd.notna(slug) and str(slug).strip() != "":
        return str(slug).replace('-', ' ').title()
    return nome_fantasia

# =============================================================================
# 1. PROCESSANDO A DIMENSÃO TIMES
# =============================================================================
print("🚀 Extraindo e processando dim_times...")
resposta_clubes = requests.get("https://api.cartola.globo.com/clubes")

if resposta_clubes.status_code == 200:
    dados_clubes = resposta_clubes.json()
    dados_clubes.pop('1', None)
    
    df_times = pd.DataFrame.from_dict(dados_clubes, orient='index')
    df_times['url_escudo'] = df_times['escudos'].apply(extrair_url_escudo)
    df_times['nome'] = df_times.apply(limpar_nome_time, axis=1)
    df_times = df_times[['id', 'nome', 'abreviacao', 'url_escudo']]
    
    # Mandando para a Nuvem
    # Limpa os dados antigos mantendo a estrutura da tabela intacta para o dbt
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM dim_times;"))

    # Insere os dados novos usando 'append' no lugar de 'replace'
    df_times.to_sql(name='dim_times', con=engine, if_exists='append', index=False)
    print("✅ dim_times salva no Supabase com sucesso!")

# =============================================================================
# 2. PROCESSANDO A FATO PARTIDAS (Carga Histórica Dinâmica)
# =============================================================================
print("🚀 Extraindo e processando fato_partidas...")
resposta_rodadas = requests.get("https://api.cartola.globo.com/rodadas")
total_rodadas = len(resposta_rodadas.json()) if resposta_rodadas.status_code == 200 else 38

url_partidas = "https://api.cartola.globo.com/partidas"
dados_fatos = []

for rodada in range(1, total_rodadas + 1):
    resposta_rodada = requests.get(f"{url_partidas}/{rodada}")
    if resposta_rodada.status_code == 200:
        jogos = resposta_rodada.json().get('partidas', [])
        for jogo in jogos:
            linha = {
                "id_partida": jogo.get('partida_id'),
                "rodada": rodada,
                "data_jogo": jogo.get('partida_data'),
                "id_time_mandante": jogo.get('clube_casa_id'),
                "id_time_visitante": jogo.get('clube_visitante_id'),
                "gols_mandante": jogo.get('placar_oficial_mandante'),
                "gols_visitante": jogo.get('placar_oficial_visitante'),
                "valida_pro_cartola": jogo.get('valida')
            }
            dados_fatos.append(linha)
    print(f"⏳ Lendo rodada {rodada}/{total_rodadas}...", end='\r')

if dados_fatos:
    df_fatos = pd.DataFrame(dados_fatos)
    # Mandando para a Nuvem
    # Limpa os dados antigos mantendo a estrutura da tabela intacta para o dbt
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM fato_partidas;"))

    # Insere os dados novos usando 'append' no lugar de 'replace'
    df_fatos.to_sql(name='fato_partidas', con=engine, if_exists='append', index=False)
    print(f"\n✅ fato_partidas ({len(df_fatos)} linhas) salva no Supabase com sucesso!")

print("🎉 ETL Finalizada! Dados 100% na Nuvem.")