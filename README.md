# ⚽ Projeto de Engenharia de Dados: Pipeline ETL - Brasileirão Série A na Nuvem

## 📌 Visão Geral do Projeto
Este projeto consiste na construção de uma pipeline de dados automatizada (ETL - *Extract, Transform, Load*) focada em dados esportivos do Campeonato Brasileiro. O objetivo é extrair dados brutos de partidas em tempo real via API, aplicar regras de Qualidade de Dados (Data Quality), e estruturar as informações em um banco de dados relacional na nuvem utilizando **Modelagem Dimensional (Star Schema)** e **Orquestração via CI/CD**.

---

## 🚨 O Problema de Negócio e a Evolução da Arquitetura
No mercado de análise esportiva, os dados chegam em formatos complexos e aninhados, e exigem atualização constante. O projeto evoluiu em fases para simular um ambiente real de Engenharia de Dados corporativa:
1.  **Refatoração para Tempo Real:** Migração de dados estáticos para consumo da API pública do Cartola FC (Globo), garantindo acesso a dados ao vivo da temporada atual sem custos.
2.  **Migração para Cloud:** Transição de um banco de dados local (SQLite) para uma infraestrutura robusta na nuvem com **PostgreSQL (Supabase)**.
3.  **Automação (DataOps):** Substituição de execuções manuais via Jupyter Notebooks por scripts Python unificados, orquestrados diariamente via **GitHub Actions**.

---

## 🏛️ Arquitetura Cloud e Modelagem (Star Schema)
O banco de dados PostgreSQL foi desenhado para garantir alta performance de leitura e escalabilidade para ferramentas de BI:
*   **`dim_times` (Dimensão):** Catálogo contendo os dados cadastrais, escudos e identificadores dos clubes.
*   **`fato_partidas` (Fato):** Tabela central focada em métricas e chaves numéricas (IDs). Contém o histórico completo (*Full Load*) de jogos já realizados e a agenda das próximas partidas, extraídos de forma dinâmica.

---

## 🛠️ Ferramentas e Tecnologias
*   **Linguagem:** Python 3 (`.py` puro empacotado para produção).
*   **Bibliotecas:** `pandas`, `requests`, `sqlalchemy`, `psycopg2-binary`, `python-dotenv`.
*   **Fonte de Dados (API):** *Cartola FC (Rede Globo)*.
*   **Banco de Dados (Cloud):** PostgreSQL hospedado no Supabase.
*   **Orquestração (CI/CD):** GitHub Actions (Cron Jobs).
*   **Governança:** Arquivo `.env` e GitHub Secrets para proteção de credenciais.

---

## 🧠 Highlights Técnicos e Decisões de Arquitetura
*   **Data Quality e Tratamento de Exceções:** Implementação de uma tabela *De-Para (Lookup Dictionary)* para padronização de grafias, siglas e acentuações corrompidas na origem.
*   **Desempacotamento de JSONs Aninhados:** Tratamento de estruturas profundas em listas e dicionários via Python e Pandas.
*   **Carga Dinâmica (Sem Magic Numbers):** O script consulta automaticamente os *endpoints* de metadados da API para descobrir a quantidade exata de rodadas, adaptando-se a mudanças no calendário de forma autônoma.
*   **Estratégia de Full Load:** Carga completa a cada execução para mapeamento de jogos adiados (*Late Arriving Facts*) e garantia de integridade temporal.
*   **Pipeline Autogerenciável:** O fluxo de trabalho no GitHub Actions garante a execução diária da coleta de dados sem intervenção humana, mantendo o *Single Source of Truth* sempre atualizado.

---

## 📊 Status do Projeto
✅ **Fase 1:** Pipeline ETL ponta a ponta estruturada.
✅ **Fase 2:** Implementação da Modelagem Dimensional (Star Schema).
✅ **Fase 3:** Refatoração para dados em tempo real (API Cartola) e Data Quality.
✅ **Fase 4:** Empacotamento de código, Migração para Supabase (PostgreSQL) e Orquestração via GitHub Actions.