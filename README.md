# Desafio MBA Engenharia de Software com IA - Full Cycle

## Como Executar o Projeto

Siga os passos abaixo para configurar e executar a solução de Ingestão e Busca Semântica (RAG).

### 1. Configuração do Ambiente

Crie um arquivo `.env` na raiz do projeto, baseado no `.env.example`, e preencha as variáveis de ambiente necessárias:

```ini
# Variáveis para a conexão com o PostgreSQL
DATABASE_URL="postgresql+psycopg2://user:password@host:port/database"
PG_VECTOR_COLLECTION_NAME="pdf_documents"

# Caminho para o arquivo PDF a ser ingerido
PDF_PATH="documents/example.pdf" # Certifique-se de que o arquivo exista

# Configuração para OpenAI (descomente e preencha se for usar OpenAI)
# OPENAI_API_KEY="sua_chave_api_openai"
# OPENAI_EMBEDDING_MODEL="text-embedding-3-small"
# OPENAI_CHAT_MODEL="gpt-3.5-turbo"

# Configuração para Google Gemini (descomente e preencha se for usar Gemini)
# GOOGLE_API_KEY="sua_chave_api_google"
# GOOGLE_EMBEDDING_MODEL="models/embedding-001"
# GOOGLE_CHAT_MODEL="gemini-pro"
```
**Nota:** Você deve fornecer uma chave de API para OpenAI ou Google Gemini, mas não para ambos simultaneamente. O sistema detectará qual provedor usar com base nas variáveis de ambiente preenchidas.

### 2. Instalação de Dependências

Certifique-se de ter o Python instalado (versão 3.9 ou superior). É altamente recomendável usar um ambiente virtual.

```bash
# Crie e ative um ambiente virtual (exemplo com venv)
python -m venv .venv
# No Windows:
.venv\\Scripts\\activate
# No macOS/Linux:
source .venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### 3. Ingestão de Dados

Execute o script de ingestão para processar o arquivo PDF e armazenar os embeddings no banco de dados vetorial.

```bash
python src/ingest.py
```

### 4. Execução do Chat RAG

Após a ingestão, você pode iniciar a aplicação de chat.

```bash
python src/chat.py
```
O chat será executado no terminal, onde você poderá digitar suas perguntas e receber respostas baseadas no contexto ingerido. Digite `sair` para encerrar o chat.