from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "emissions_global.txt"
VECTOR_DB_DIR = BASE_DIR / "data" / "chroma_db"


def build_rag_chain():
    # 1. Load knowledge base
    loader = TextLoader(str(DATA_FILE), encoding="utf-8")
    documents = loader.load()

    # 2. Split text into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    docs = splitter.split_documents(documents)

    # 3. Create embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # 4. Create / load vector store
    vectorstore = Chroma(
        persist_directory=str(VECTOR_DB_DIR),
        embedding_function=embeddings
    )
    vectorstore.add_documents(docs)
    vectorstore.persist()

    # 5. Load IBM Granite via Ollama
    llm = OllamaLLM(
        model="granite3-dense:8b",
        base_url="http://localhost:11434"
    )

    # 6. Build RAG chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        chain_type="stuff"
    )

    return qa_chain
