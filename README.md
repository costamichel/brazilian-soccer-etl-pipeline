# ⚽ Projeto End-to-End: Engenharia de Dados e Analytics - Brasileirão Série A

**Acesse o Dashboard Interativo Ao Vivo:** [🔗 https://share.streamlit.io/]

## 📌 Visão Geral do Projeto
Este projeto consiste na construção de uma arquitetura completa de dados ponta a ponta (do *Backend* ao *Frontend* Analítico). O objetivo é extrair dados brutos de partidas em tempo real via API, processá-los na nuvem utilizando **Modelagem Dimensional (Star Schema)**, orquestrar atualizações automáticas diárias e, por fim, disponibilizar as métricas em uma **Aplicação Web Interativa (Business Intelligence)**.

---

## 🚨 Evolução da Arquitetura e Fases do Projeto
O projeto foi desenvolvido em ciclos para simular o ecossistema completo de uma infraestrutura corporativa moderna:
1.  **Ingestão e Tempo Real:** Consumo dinâmico da API pública do Cartola FC (Globo), lidando com paginação e desempacotamento de JSONs aninhados.
2.  **Modelagem e Cloud:** Transição de arquivos locais para um Data Warehouse na nuvem utilizando **PostgreSQL (Supabase)**, estruturado em Tabelas Fato e Dimensão.
3.  **Automação (DataOps):** Orquestração CI/CD via **GitHub Actions** (Cron Jobs) para execução diária autônoma, garantindo a atualização do banco de dados (Single Source of Truth) sem intervenção humana.
4.  **Business Intelligence (Analytics):** Construção de um Dashboard interativo em Python utilizando **Streamlit**, com filtros dinâmicos e cálculos de KPIs esportivos em tempo real, hospedado na nuvem (Streamlit Community Cloud).

---

## 🛠️ Ferramentas e Tecnologias
*   **Linguagem:** Python 3 (Scripts ETL puros e Frontend Web).
*   **Bibliotecas Principais:** `pandas`, `requests`, `sqlalchemy`, `psycopg2-binary`, `streamlit`.
*   **Fonte de Dados:** *API Cartola FC (Rede Globo)*.
*   **Banco de Dados (Cloud):** PostgreSQL (Supabase).
*   **Orquestração e CI/CD:** GitHub Actions.
*   **Hospedagem Web:** Streamlit Community Cloud.

---

## 🧠 Highlights Técnicos
*   **Data Quality e Tratamento:** Implementação de *Lookup Dictionaries* para padronização de grafias e siglas corrompidas na origem.
*   **Estratégia de Resiliência (Idempotência):** Carga completa (*Full Load*) a cada execução para mapeamento perfeito de jogos adiados (*Late Arriving Facts*) e garantia de integridade estrutural.
*   **Performance de Frontend:** Uso de decorators como `@st.cache_data` para armazenar consultas em memória RAM, otimizando o carregamento da aplicação web e evitando sobrecarga no banco de dados.
*   **Métricas Dinâmicas:** A aplicação recalcula em frações de segundo os *KPIs* (Gols Marcados, Sofridos e Saldo) baseando-se no contexto selecionado (Mandante ou Visitante) através do Pandas.
*   **Governança e Segurança:** Proteção de credenciais (Connection Strings) utilizando `.env` localmente e injeção via **Secrets** tanto no GitHub Actions quanto no Streamlit Cloud.

---

## 📊 Status do Projeto
✅ **Fase 1:** Pipeline ETL estruturada.
✅ **Fase 2:** Modelagem Dimensional (Star Schema).
✅ **Fase 3:** Refatoração para dados da API ao vivo.
✅ **Fase 4:** Migração para Postgres na Nuvem e Orquestração (GitHub Actions).
✅ **Fase 5:** Desenvolvimento e Deploy do Dashboard Interativo (Streamlit).
🚀 **Status:** Concluído e operando em produção.