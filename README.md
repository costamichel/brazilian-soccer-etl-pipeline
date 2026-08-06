# ⚽ Projeto de Engenharia de Dados: Pipeline ETL - Brasileirão Série A

## 📌 Visão Geral do Projeto
Este projeto consiste na construção de uma pipeline de dados automatizada (ETL - *Extract, Transform, Load*) focada em dados esportivos. O objetivo é extrair dados brutos de partidas do Campeonato Brasileiro, tratar as inconsistências e aninhamentos do formato JSON, e carregar essas informações estruturadas em um banco de dados relacional local, disponibilizando uma base limpa e pronta para o consumo de Analistas e Cientistas de Dados.

## 🚨 O Problema de Negócio
No mercado de análise esportiva (Scout e Performance), os dados gerados pelas partidas frequentemente chegam em formatos complexos, desestruturados e com múltiplas camadas (JSONs profundos). Profissionais de dados perdem muito tempo com a limpeza manual antes de conseguirem gerar inteligência. Este projeto cria o "motor invisível" que resolve a ingestão, transformando o caos de dados brutos em tabelas relacionais organizadas de forma 100% programática.

## 🛠️ Arquitetura e Ferramentas
*   **Linguagem:** Python 3 (uso de Jupyter Notebooks `.ipynb` para execução modularizada).
*   **Fonte de Dados (API):** *API-Sports* (conexão direta via `api-sports.io`).
*   **Bibliotecas (Python):** 
    *   `requests`: Comunicação web e extração via protocolo HTTP.
    *   `pandas`: Motor de transformação, limpeza e modelagem dos dados (DataFrames).
    *   `python-dotenv`: Gerenciamento de variáveis de ambiente para proteção de credenciais.
*   **Armazenamento (Banco de Dados):** SQLite (Banco relacional embutido e local).
*   **Auditoria de Dados:** DBeaver (Visualização e validação das tabelas via SQL).

## 🚀 Como Executar o Projeto

### 1. Pré-requisitos
Certifique-se de ter o Python instalado e instale as bibliotecas necessárias:
pip install pandas requests python-dotenv

### 2. Configuração de Credenciais (Segurança)
Para rodar este projeto, você precisará de uma Chave de API gratuita da API-Sports.
1. Crie uma conta em api-sports.io.
2. Na raiz do projeto, crie um arquivo chamado `.env`.
3. Adicione a sua chave no arquivo no seguinte formato:
API_KEY_FOOTBALL=sua_chave_de_api_aqui

*Nota: O repositório já conta com um `.gitignore` configurado para impedir o vazamento do arquivo `.env`.*

### 3. Executando a Pipeline
Abra o arquivo `extracao_brasileirao.ipynb` em sua IDE (recomendado: VS Code) e execute as células sequencialmente para observar as três etapas do processo (ETL).

## 🧠 Decisões de Arquitetura e Soluções (Highlights do Projeto)

*   **Bypass de Agregadores:** Em vez de utilizar serviços intermediários (como RapidAPI), a extração foi refatorada para consumir os endpoints diretamente da documentação oficial da API-Sports, garantindo maior estabilidade e controle dos *Headers* de autenticação.
*   **Tratamento de Regras de Negócio (Tier Limits):** O plano gratuito da API restringe o acesso a temporadas correntes. A pipeline foi adaptada para extrair os dados da temporada histórica de 2023, provando a robustez da arquitetura que funciona independentemente do ano consultado.
*   **Segurança de Credenciais:** Implementação da biblioteca `dotenv` para isolar a chave da API do código-fonte, garantindo boas práticas de Engenharia de Software e segurança da informação.
*   **Carga Idempotente:** A inserção no banco de dados SQLite utiliza o parâmetro `if_exists='replace'` do Pandas, permitindo que a pipeline seja executada múltiplas vezes sem gerar duplicidade de registros na tabela final.

## 📊 Status do Projeto
✅ **Fase 1 (Concluída):** Pipeline ETL ponta a ponta finalizada com sucesso. Dados persistidos em formato tabular no banco local (`banco_brasileirao.db`).