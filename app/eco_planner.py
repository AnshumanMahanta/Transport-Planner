from langchain_ollama import ChatOllama
from langchain.chains import RetrievalQA
from app.knowledge_base import build_vector_db

def create_eco_planner(knowledge_text: str):
    vector_db = build_vector_db(knowledge_text)

    llm = ChatOllama(
        model="granite3-dense:8b",
        temperature=0
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_db.as_retriever(k=2),
    )

    return qa_chain
