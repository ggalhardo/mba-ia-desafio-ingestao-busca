import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings

def ingest_pdf():
    # 1. Carregar o PDF dinamicamente a partir da env
    pdf_path = os.getenv("PDF_PATH", "document.pdf")
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    
    # 2. Dividir em chunks controlados
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = text_splitter.split_documents(documents)
    
    # 3. Configurações do Banco Vetorial vindas da env
    connection_string = os.getenv("DATABASE_URL")
    collection_name = os.getenv("PG_VECTOR_COLLECTION_NAME", "pdf_documents")
    
    # 4. Identificar o provedor de embedding correto e seu respectivo modelo configurado
    if os.getenv("OPENAI_API_KEY"):
        model_name = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
        embeddings = OpenAIEmbeddings(model=model_name)
    else:
        model_name = os.getenv("GOOGLE_EMBEDDING_MODEL", "models/embedding-001")
        embeddings = GoogleGenerativeAIEmbeddings(model=model_name)
        
    # 5. Ingestão para o pgVector
    vector_store = PGVector.from_documents(
        documents=chunks,
        embedding=embeddings,
        connection=connection_string,
        collection_name=collection_name,
        use_jsonb=True
    )
    print(f"Sucesso: {len(chunks)} fragmentos ingeridos na coleção '{collection_name}'.")

if __name__ == "__main__":
    ingest_pdf()