import os
from langchain_ollama import ChatOllama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA

# --- 1. THE KNOWLEDGE BASE ---
# India-specific emission factors (2024-2025 Data)
SUSTAINABILITY_HANDBOOK = """
EcoRoute Knowledge Base - Indian Transport Emissions:
1. Private SUV (Petrol): Emits 0.213 kg of CO2 per km.
2. Small Hatchback (Petrol): Emits 0.111 kg of CO2 per km.
3. Motorcycle (<125cc): Emits 0.032 kg of CO2 per km.
4. Electric Bus (Indian Grid): Emits roughly 0.012 kg of CO2 per passenger-km.
5. CNG Public Bus: Emits 0.053 kg of CO2 per passenger-km.
6. Metro Rail: The greenest option, emitting only 0.011 kg of CO2 per passenger-km.
7. Walking/Cycling: Zero emissions.
Note: For a 10km trip, an SUV emits 2.13kg CO2, while a Metro trip emits only 0.11kg.
"""

def build_eco_planner():
    print("--- Initializing EcoRoute Local AI (IBM Granite) ---")
    
    # --- 2. SETUP RAG (Vector Database) ---
    # Convert our handbook into searchable chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
    docs = text_splitter.split_text(SUSTAINABILITY_HANDBOOK)
    
    # Use HuggingFace for free local embeddings (converts text to numbers)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Create an in-memory vector database
    vector_db = Chroma.from_texts(docs, embeddings)
    retriever = vector_db.as_retriever(search_kwargs={"k": 2})

    # --- 3. INITIALIZE LOCAL MODEL ---
    # Connects to your running Ollama instance
    llm = ChatOllama(model="granite3-dense:8b", temperature=0)

    # --- 4. CREATE THE ASSISTANT CHAIN ---
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm, 
        chain_type="stuff", 
        retriever=retriever
    )
    
    return qa_chain

# --- 5. MAIN INTERFACE ---
if __name__ == "__main__":
    planner = build_eco_planner()
    
    print("\nWelcome to EcoRoute! I can help you plan the greenest commute.")
    print("Example: 'I want to travel 15km. Should I take a Petrol SUV or a Bus?'")
    
    while True:
        user_query = input("\n[User]: ")
        if user_query.lower() in ['exit', 'quit']:
            break
            
        print("\n[EcoRoute Assistant is thinking...]")
        response = planner.run(user_query)
        print(f"\n[Assistant]: {response}")

# --- RESPONSIBLE AI NOTE ---
# This system is 'Transparent' because it uses a specific Knowledge Base 
# grounded in Indian transport data, preventing the AI from hallucinating numbers.