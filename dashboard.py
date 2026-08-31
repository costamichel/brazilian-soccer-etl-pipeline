import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# =============================================================================
# 1. CONFIGURAÇÃO DA PÁGINA
# =============================================================================
st.set_page_config(layout="wide", page_title="Dashboard Brasileirão 2026", page_icon="⚽")

# --- Link para o GitHub na Barra Lateral ---
st.sidebar.markdown("---")
st.sidebar.markdown("### 👨‍💻 Código Fonte")
st.sidebar.markdown("Gostou do projeto? Veja a arquitetura e o código completo no repositório:")

# Botão nativo do Streamlit
st.sidebar.link_button("🔗 Acessar GitHub", "https://github.com/costamichel/brazilian-soccer-etl-pipeline")

st.sidebar.markdown("---")

st.title("⚽ Painel Analítico - Brasileirão Série A")
st.markdown("Acompanhe os resultados e métricas em tempo real direto do banco de dados na nuvem.")

# =============================================================================
# 2. CONEXÃO COM BANCO DE DADOS (USANDO CACHE E SECRETS NATIVOS)
# =============================================================================
# O cache expira automaticamente a cada 1 hora (3600 segundos)
@st.cache_data(ttl=3600)
def carregar_dados():
    load_dotenv()
    
    # 1. Tenta pegar a variável do Streamlit Secrets (Nuvem)
    if "DATABASE_URL" in st.secrets:
        db_url = st.secrets["DATABASE_URL"]
    # 2. Se não achar, tenta pegar do arquivo .env (Local)
    else:
        db_url = os.getenv("DATABASE_URL")
    
    # Trava de segurança para avisar se a senha realmente sumiu
    if not db_url:
        st.error("🚨 Erro: A String de Conexão não foi encontrada nas Secrets.")
        st.stop()
        
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
        
    engine = create_engine(db_url)
    
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
    WHERE f.gols_mandante IS NOT NULL
    ORDER BY f.rodada DESC, f.data_jogo DESC;
    """
    
    df = pd.read_sql(query, engine)
    
    df['gols_mandante'] = df['gols_mandante'].astype(int)
    df['gols_visitante'] = df['gols_visitante'].astype(int)
    df['rodada'] = df['rodada'].astype(int)
    
    return df

df_jogos = carregar_dados()

# =============================================================================
# 3. BARRA LATERAL (FILTROS)
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
# 4. CARTÕES DE MÉTRICAS (KPIs DINÂMICOS)
# =============================================================================
total_jogos = len(df_filtrado)

if time_selecionado != "Todos os Times":
    # Lógica isolada para o time selecionado
    gols_marcados = int(
        df_filtrado.loc[df_filtrado['mandante'] == time_selecionado, 'gols_mandante'].sum() + 
        df_filtrado.loc[df_filtrado['visitante'] == time_selecionado, 'gols_visitante'].sum()
    )
    
    gols_sofridos = int(
        df_filtrado.loc[df_filtrado['mandante'] == time_selecionado, 'gols_visitante'].sum() + 
        df_filtrado.loc[df_filtrado['visitante'] == time_selecionado, 'gols_mandante'].sum()
    )
    
    saldo_gols = gols_marcados - gols_sofridos
    
    # Criando 4 colunas para a visualização específica do clube
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="📊 Partidas Jogadas", value=total_jogos)
    with col2:
        st.metric(label="⚽ Gols Marcados (Pró)", value=gols_marcados)
    with col3:
        st.metric(label="🥅 Gols Sofridos (Contra)", value=gols_sofridos)
    with col4:
        st.metric(label="📈 Saldo de Gols", value=saldo_gols)

else:
    # Lógica geral para o campeonato inteiro
    total_gols = int(df_filtrado['gols_mandante'].sum() + df_filtrado['gols_visitante'].sum())
    media_gols = (total_gols / total_jogos) if total_jogos > 0 else 0
    
    # Criando 3 colunas para a visão geral
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="📊 Total de Jogos", value=total_jogos)
    with col2:
        st.metric(label="⚽ Gols no Campeonato", value=total_gols)
    with col3:
        st.metric(label="🎯 Média de Gols/Jogo", value=f"{media_gols:.2f}")

st.markdown("---")

# =============================================================================
# 5. TABELA DE RESULTADOS
# =============================================================================
st.subheader(f"📋 Histórico de Partidas - {time_selecionado}")

df_exibicao = df_filtrado.copy()
df_exibicao['Placar'] = df_exibicao['gols_mandante'].astype(str) + " x " + df_exibicao['gols_visitante'].astype(str)
df_exibicao = df_exibicao[['rodada', 'data', 'mandante', 'Placar', 'visitante']]
df_exibicao.columns = ['Rodada', 'Data', 'Mandante', 'Placar', 'Visitante']

st.dataframe(df_exibicao, use_container_width=True, hide_index=True)