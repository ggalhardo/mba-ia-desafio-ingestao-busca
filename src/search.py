import os
from langchain_postgres import PGVector
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def search_prompt(question=None):
    connection_string = os.getenv("DATABASE_URL")
    collection_name = os.getenv("PG_VECTOR_COLLECTION_NAME", "pdf_documents")

    if os.getenv("OPENAI_API_KEY"):
        embedding_model_name = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
        embeddings = OpenAIEmbeddings(model=embedding_model_name)
        llm_model_name = os.getenv("OPENAI_CHAT_MODEL", "gpt-3.5-turbo")
        llm = ChatOpenAI(model=llm_model_name, temperature=0)
    else:
        embedding_model_name = os.getenv("GOOGLE_EMBEDDING_MODEL", "models/embedding-001")
        embeddings = GoogleGenerativeAIEmbeddings(model=embedding_model_name)
        llm_model_name = os.getenv("GOOGLE_CHAT_MODEL", "gemini-2.5-flash")
        llm = ChatGoogleGenerativeAI(model=llm_model_name, temperature=0)

    vector_store = PGVector(collection_name=collection_name, connection=connection_string, embeddings=embeddings)
    retriever = vector_store.as_retriever()
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    rag_chain = (
        {"contexto": retriever, "pergunta": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain.invoke(question)