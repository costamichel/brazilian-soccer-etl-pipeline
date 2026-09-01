# ⚽ Projeto End-to-End: Engenharia de Dados e Analytics - Brasileirão Série A

**Acesse o Dashboard Interativo Ao Vivo:** [🔗 https://brasileirao-analytics.streamlit.app/]

## 📌 Visão Geral do Projeto
Este projeto consiste na construção de uma arquitetura completa de dados ponta a ponta (do *Backend* ao *Frontend* Analítico). O objetivo é extrair dados brutos de partidas em tempo real via API, transformá-los e modelá-los utilizando **dbt (data build tool)** na nuvem, orquestrar atualizações automáticas e disponibilizar as métricas em uma **Aplicação Web Interativa (Business Intelligence)**.

---

## 🚨 Evolução da Arquitetura e Fases do Projeto
O projeto foi desenvolvido em ciclos para simular o ecossistema completo de uma infraestrutura corporativa (Modern Data Stack):
1.  **Ingestão e Tempo Real:** Consumo dinâmico da API pública do Cartola FC (Globo), lidando com paginação e desempacotamento de JSONs aninhados.
2.  **Armazenamento Cloud:** Armazenamento dos dados brutos num Data Warehouse utilizando **PostgreSQL (Supabase)**.
3.  **Transformação com dbt (Analytics Engineering):** Substituição de regras de negócio em Python/Pandas por modelos declarativos SQL no **dbt**. Implementação de arquitetura multi-camadas (Staging e Marts), garantindo materialização em views e tabelas (`mart_partidas_enriquecidas`, `mart_classificacao`).
4.  **Automação (DataOps):** Orquestração CI/CD via **GitHub Actions** (Cron Jobs) executando o pipeline completo: ingestão Python e run das transformações do dbt, garantindo atualização diária sem intervenção humana.
5.  **Business Intelligence (Analytics):** Construção de um Dashboard interativo em Python utilizando **Streamlit**, lendo diretamente as tabelas consolidadas geradas pelo dbt. 

---

## 🛠️ Ferramentas e Tecnologias
*   **Linguagem:** Python 3 (Ingestão e Frontend Web) e SQL (dbt).
*   **Transformação e Modelagem:** dbt (data build tool).
*   **Bibliotecas Principais:** `pandas`, `requests`, `sqlalchemy`, `psycopg2-binary`, `streamlit`.
*   **Fonte de Dados:** *API Cartola FC (Rede Globo)*.
*   **Banco de Dados (Cloud):** PostgreSQL (Supabase).
*   **Orquestração e CI/CD:** GitHub Actions.
*   **Hospedagem Web:** Streamlit Community Cloud.

---

## 🧠 Highlights Técnicos
*   **Separação de Responsabilidades (ETL vs ELT):** Com a introdução do dbt, a ingestão Python ficou responsável apenas pelo Load bruto. Toda a lógica de negócio (como cálculos complexos via *Window Functions* para criar a tabela de classificação) foi migrada para a camada de Analytics Engineering (Marts do dbt).
*   **Arquitetura Visual Modular:** O frontend (Streamlit) utiliza o recurso de `st.tabs` para separar visões de negócio ("Classificação Geral" e "Partidas e Resultados") garantindo uma UX fluida e sem poluição visual num dashboard de única página.
*   **Estratégia de Resiliência (Idempotência):** Carga completa (*Full Load*) a cada execução para mapeamento perfeito de jogos adiados (*Late Arriving Facts*) na camada bruta, combinada com reconstrução diária dos modelos do dbt.
*   **Performance de Frontend:** Uso de decorators como `@st.cache_data` para armazenar consultas em memória RAM, otimizando o carregamento da aplicação web e evitando sobrecarga no banco de dados.
*   **Governança e Segurança:** Proteção de credenciais utilizando `.env` localmente e injeção via **Secrets** em múltiplos ambientes (GitHub Actions, dbt `profiles.yml` dinâmico e Streamlit Cloud).

---

## 📊 Status do Projeto
✅ **Fase 1:** Pipeline de Ingestão Python estruturada.
✅ **Fase 2:** Transição para o Banco de Dados Nuvem (Supabase).
✅ **Fase 3:** Implementação do **dbt** para criação das camadas Staging e Marts (Modelagem Dimensional).
✅ **Fase 4:** Orquestração End-to-End no GitHub Actions (Python -> dbt).
✅ **Fase 5:** Desenvolvimento e Deploy do Dashboard Streamlit com Abas de Partidas e Nova Tabela de Classificação.
🚀 **Status:** Concluído, documentado e operando em produção.