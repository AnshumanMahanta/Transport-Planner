import streamlit as st
from pathlib import Path
from langchain_ollama import OllamaLLM
import numpy as np

# --- Base paths ---
BASE_DIR = Path(__file__).parent
DATA_FILES = [
    BASE_DIR / "data" / "emissions_global.txt",
    BASE_DIR / "data" / "sustainability_handbook.txt",
    BASE_DIR / "kb" / "transport_knowledge.txt"
]

# --- Streamlit config ---
st.set_page_config(
    page_title="EcoTravel-GPT",
    page_icon="",
    layout="wide"
)
st.title("EcoTravel-GPT")
st.write("Plan your commute sustainably and efficiently.\n")

# --- Load all text files ---
all_text = ""
for file_path in DATA_FILES:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            all_text += f.read() + "\n\n"
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")

# --- Simple in-memory RAG setup ---
chunk_size = 500
docs = [all_text[i:i+chunk_size] for i in range(0, len(all_text), chunk_size)]

def embed_text(text):
    """Simple numeric embedding using character ordinals (demo purpose)"""
    vec = np.zeros(300)
    for i, c in enumerate(text[:300]):
        vec[i] = ord(c)
    return vec

# Precompute embeddings
doc_embeddings = [embed_text(doc) for doc in docs]

def query_rag(user_query):
    query_vec = embed_text(user_query)
    # Cosine similarity
    sims = [np.dot(query_vec, de)/(np.linalg.norm(query_vec)*np.linalg.norm(de)) for de in doc_embeddings]
    return docs[np.argmax(sims)]

# --- Ollama LLM ---
llm = OllamaLLM(model="granite3-dense:8b", base_url="http://localhost:11434")

# --- User input ---
st.subheader("Ask about green transport")
user_input = st.text_input("Enter your question:")

if st.button("Get Answer"):
    if not user_input:
        st.warning("Please type a question first!")
    else:
        # Retrieve context from RAG
        context = query_rag(user_input)
        prompt = f"Answer the question using the following context:\n\nContext:\n{context}\n\nQuestion:\n{user_input}"

        # Get response from Ollama
        try:
            response = llm.invoke(prompt)
            st.subheader("Answer from IBM Granite Model")
            st.write(response)
        except Exception as e:
            st.error(f"Error connecting to Ollama: {e}")
