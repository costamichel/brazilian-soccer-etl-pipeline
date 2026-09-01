import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# =============================================================================
# 1. CONFIGURAÇÃO DA PÁGINA (Mantido igual)
# =============================================================================
st.set_page_config(layout="wide", page_title="Dashboard Brasileirão 2026", page_icon="⚽")

st.sidebar.markdown("---")
st.sidebar.markdown("### 👨‍💻 Código Fonte")
st.sidebar.link_button("🔗 Acessar GitHub", "https://github.com/costamichel/brazilian-soccer-etl-pipeline")
st.sidebar.markdown("---")

st.title("⚽ Painel Analítico - Brasileirão Série A")
st.markdown("Acompanhe os resultados e métricas em tempo real direto do banco de dados na nuvem.")

# =============================================================================
# 2. CONEXÃO E CARREGAMENTO DE DADOS
# =============================================================================
# Isolamos a criação da engine para reutilizar nas duas consultas
@st.cache_resource 
def get_engine():
    load_dotenv()
    db_url = st.secrets.get("DATABASE_URL") or os.getenv("DATABASE_URL")
    
    if not db_url:
        st.error("🚨 Erro: A String de Conexão não foi encontrada.")
        st.stop()
        
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
        
    return create_engine(db_url)

# Função atual de partidas (mantida igual, só usando a nova engine)
@st.cache_data(ttl=3600)
def carregar_partidas():
    engine = get_engine()
    query = """
    SELECT 
        f.rodada,
        SUBSTR(f.data_jogo, 1, 10) AS data,
        t_mandante.nome AS mandante,
        f.gols_mandante,
        f.gols_visitante,
        t_visitante.nome AS visitante
    FROM dbt_dev.mart_partidas_enriquecidas f
    JOIN dim_times t_mandante ON f.id_time_mandante = t_mandante.id
    JOIN dim_times t_visitante ON f.id_time_visitante = t_visitante.id
    WHERE f.gols_mandante IS NOT NULL   -- isso traz somente partidas que já aconteceram
    ORDER BY f.rodada DESC, f.data_jogo DESC;
    """
    df = pd.read_sql(query, engine)
    df['gols_mandante'] = df['gols_mandante'].astype(int)
    df['gols_visitante'] = df['gols_visitante'].astype(int)
    df['rodada'] = df['rodada'].astype(int)
    return df

# NOVA FUNÇÃO: Carregar a classificação
@st.cache_data(ttl=3600)
def carregar_classificacao():
    engine = get_engine()
    query = """SELECT 
            posicao as posicao,
            nome as time, 
            pontos as pontos,
            vitorias as vitorias,
            saldo_gols as saldo_gols, 
            empates as empates,
            derrotas as derrotas,
            gols_pro as gols_pro,
            gols_contra as gols_contra
        FROM dbt_dev.mart_classificacao 
        ORDER BY posicao ASC
        ;
    """
    return pd.read_sql(query, engine)

df_jogos = carregar_partidas()
df_classificacao = carregar_classificacao()
print(df_classificacao.head())

# =============================================================================
# 3. BARRA LATERAL (FILTROS - Mantido igual)
# =============================================================================
st.sidebar.header("🔍 Filtros de Pesquisa")
lista_times = sorted(list(set(df_jogos['mandante'].unique()).union(set(df_jogos['visitante'].unique()))))
lista_times.insert(0, "Todos os Times")
time_selecionado = st.sidebar.selectbox("Selecione um Clube:", lista_times)

if time_selecionado != "Todos os Times":
    df_filtrado = df_jogos[
        (df_jogos['mandante'] == time_selecionado) | 
        (df_jogos['visitante'] == time_selecionado)
    ]
else:
    df_filtrado = df_jogos.copy()

# =============================================================================
# 4. ORGANIZAÇÃO EM ABAS (NOVA ARQUITETURA VISUAL)
# =============================================================================
# Criamos as abas aqui
aba_classificacao, aba_partidas = st.tabs(["🏆 Classificação", "📋 Partidas e Resultados"])

# CONTEÚDO DA ABA 1
with aba_classificacao:
    st.subheader("Classificação Geral")
    
    # Cria uma cópia para exibição sem afetar o cache original
    df_class_exibicao = df_classificacao.copy()
    
    # Reorganiza a ordem das colunas (trazendo empates e derrotas antes dos gols)
    df_class_exibicao = df_class_exibicao[['posicao', 'time', 'pontos', 'vitorias', 'empates', 'derrotas', 'gols_pro', 'gols_contra', 'saldo_gols']]
    
    # Aplica os nomes amigáveis
    df_class_exibicao.columns = ['Pos', 'Clube', 'PTS', 'V', 'E', 'D', 'GP', 'GC', 'SG']
    
    if time_selecionado != "Todos os Times":
        def highlight_team(row):
            # Atualizamos a chave de busca de 'time' para 'Clube'
            if row['Clube'] == time_selecionado: 
                return ['background-color: #e0f2fe; color: #0f172a; font-weight: bold'] * len(row)
            return [''] * len(row)
        
        st.dataframe(df_class_exibicao.style.apply(highlight_team, axis=1), use_container_width=True, hide_index=True)
    else:
        st.dataframe(df_class_exibicao, use_container_width=True, hide_index=True)

# CONTEÚDO DA ABA 2
with aba_partidas:
    total_jogos = len(df_filtrado)

    if time_selecionado != "Todos os Times":
        gols_marcados = int(df_filtrado.loc[df_filtrado['mandante'] == time_selecionado, 'gols_mandante'].sum() + df_filtrado.loc[df_filtrado['visitante'] == time_selecionado, 'gols_visitante'].sum())
        gols_sofridos = int(df_filtrado.loc[df_filtrado['mandante'] == time_selecionado, 'gols_visitante'].sum() + df_filtrado.loc[df_filtrado['visitante'] == time_selecionado, 'gols_mandante'].sum())
        saldo_gols = gols_marcados - gols_sofridos
        
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric(label="📊 Partidas", value=total_jogos)
        with col2: st.metric(label="⚽ Gols (Pró)", value=gols_marcados)
        with col3: st.metric(label="🥅 Gols (Contra)", value=gols_sofridos)
        with col4: st.metric(label="📈 Saldo", value=saldo_gols)
    else:
        total_gols = int(df_filtrado['gols_mandante'].sum() + df_filtrado['gols_visitante'].sum())
        media_gols = (total_gols / total_jogos) if total_jogos > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        with col1: st.metric(label="📊 Total de Jogos", value=total_jogos)
        with col2: st.metric(label="⚽ Gols", value=total_gols)
        with col3: st.metric(label="🎯 Média Gols/Jogo", value=f"{media_gols:.2f}")

    st.markdown("---")

    st.subheader(f"📋 Histórico de Partidas - {time_selecionado}")
    df_exibicao = df_filtrado.copy()
    df_exibicao['Placar'] = df_exibicao['gols_mandante'].astype(str) + " x " + df_exibicao['gols_visitante'].astype(str)
    df_exibicao = df_exibicao[['rodada', 'data', 'mandante', 'Placar', 'visitante']]
    df_exibicao.columns = ['Rodada', 'Data', 'Mandante', 'Placar', 'Visitante']

    st.dataframe(df_exibicao, use_container_width=True, hide_index=True)