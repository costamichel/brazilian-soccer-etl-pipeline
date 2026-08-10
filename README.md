# ⚽ Projeto de Engenharia de Dados: Pipeline ETL - Brasileirão Série A

## 📌 Visão Geral do Projeto
Este projeto consiste na construção de uma pipeline de dados automatizada (ETL - *Extract, Transform, Load*) focada em dados esportivos. O objetivo é extrair dados brutos de partidas do Campeonato Brasileiro, tratar as inconsistências e aninhamentos do formato JSON, e estruturar as informações em um banco de dados relacional local utilizando **Modelagem Dimensional (Star Schema)**, disponibilizando uma base otimizada e pronta para o consumo analítico.

## 🚨 O Problema de Negócio
No mercado de análise esportiva (Scout e Performance), os dados gerados pelas partidas chegam em formatos complexos e desestruturados (JSONs profundos). Profissionais de dados perdem tempo com limpezas manuais, e entregas em "tabelões" monolíticos causam redundância e baixa performance em consultas analíticas. Este projeto resolve isso separando o contexto (catálogos) dos eventos (fatos) de forma 100% programática.

## 🏛️ Arquitetura e Modelagem Dimensional (Star Schema)
O projeto evoluiu de uma única tabela plana para um **Modelo Estrela**, garantindo alta performance de leitura, manutenibilidade e escalabilidade:
*   **`dim_times` (Dimensão):** Catálogo contendo os dados cadastrais e identificadores dos clubes.
*   **`dim_estadios` (Dimensão):** Catálogo contendo as informações de locais e cidades dos jogos.
*   **`fato_partidas` (Fato):** Tabela central focada em métricas e chaves numéricas (IDs), registrando os eventos das partidas e conectando-se diretamente às dimensões.

## 🛠️ Ferramentas Utilizadas
*   **Linguagem:** Python 3 (Jupyter Notebooks `.ipynb`).
*   **Fonte de Dados (API):** *API-Sports* (conexão direta via `api-sports.io`).
*   **Bibliotecas (Python):** 
    *   `requests`: Comunicação web e extração HTTP.
    *   `pandas`: Transformação e modelagem de dados.
    *   `python-dotenv`: Gerenciamento seguro de variáveis de ambiente.
*   **Armazenamento (Banco de Dados):** SQLite (Banco relacional local).
*   **Auditoria de Dados:** DBeaver (Validação estrutural e consultas via SQL com `JOIN`).

## 🚀 Como Executar o Projeto

### 1. Pré-requisitos
Certifique-se de ter o Python instalado e instale as dependências:
pip install pandas requests python-dotenv

### 2. Configuração de Credenciais (Segurança)
Para rodar este projeto, você precisará de uma Chave de API gratuita da API-Sports.
1. Crie uma conta em api-sports.io.
2. Na raiz do projeto, crie um arquivo chamado `.env`.
3. Adicione a sua chave:
API_KEY_FOOTBALL=sua_chave_de_api_aqui

*Nota: O repositório conta com um `.gitignore` configurado para impedir o vazamento do arquivo `.env`.*

### 3. Executando a Pipeline
Execute os notebooks de extração e carga para popular as tabelas dimensionais e a tabela fato no banco SQLite local (`banco_brasileirao.db`).

## 🧠 Highlights Técnicos e Decisões de Arquitetura
*   **Bypass de Agregadores:** Consumo direto dos endpoints da API-Sports, garantindo maior estabilidade de autenticação por *Headers*.
*   **Modelagem Estrela (Star Schema):** Desacoplamento de atributos textuais em tabelas de dimensões dedicadas, reduzindo redundância e otimizando a performance de cruzamentos (`JOIN`).
*   **Segurança de Credenciais:** Isolamento de chaves sensíveis utilizando variáveis de ambiente (`python-dotenv`).
*   **Carga Idempotente:** Utilização de parâmetros de substituição controlada no Pandas para evitar duplicidade na persistência dos dados relacionais.

## 📊 Status do Projeto
✅ **Fase 1 (Concluída):** Pipeline ETL ponta a ponta e estruturação inicial.
✅ **Fase 2 (Concluída):** Implementação da Modelagem Dimensional (`dim_times`, `dim_estadios` e `fato_partidas`) validada via SQL no DBeaver.