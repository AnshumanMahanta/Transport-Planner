'''
ECOROUTE PROJECT – SETUP GUIDE (WINDOWS)

1. PROJECT GOAL
---------------
Build a local AI-based Green Transport Planner using:
- LangChain (RAG)
- Chroma Vector DB
- HuggingFace Embeddings
- IBM Granite model via Ollama
- Fully offline, responsible AI


2. PROJECT DIRECTORY
--------------------
D:\IBM Internship\Transport Planner\

Inside this folder:
- ecoenv/           (Python virtual environment)
- main.py           (main app file)
- app/              (modules)
- data/             (knowledge base)


3. PYTHON VIRTUAL ENVIRONMENT
-----------------------------
Create virtual environment:
> python -m venv ecoenv

Activate (PowerShell):
> ecoenv\Scripts\activate

If activation fails due to security policy:
Run PowerShell as Administrator:
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Type Y and press Enter.


4. PYTHON PACKAGE SETUP
----------------------
Upgrade pip tools:
> python -m pip install --upgrade pip setuptools wheel

Install required libraries:
> pip install langchain langchain-community langchain-ollama chromadb sentence-transformers huggingface-hub

NOTE:
- pandas, openai, streamlit are NOT required at this stage
- pandas error happened because Windows tried to compile it (no C++ tools)


5. OLLAMA SETUP (IMPORTANT)
--------------------------
Ollama was NOT installed initially, causing:
"ollama is not recognized" error.

Steps to fix:

1. Download Ollama for Windows:
   https://ollama.com/download/windows

2. Install Ollama normally

3. RESTART THE PC (mandatory)

4. Verify installation:
   > ollama --version

5. Start Ollama server:
   > ollama serve

Expected output:
   Listening on http://127.0.0.1:11434

Leave this terminal OPEN.


6. DOWNLOAD IBM GRANITE MODEL
----------------------------
Open a NEW PowerShell window:

> ollama pull granite3-dense:8b

(This downloads the IBM Granite 8B model)


7. WHY ERRORS HAPPENED
---------------------
- pandas error → Windows missing Visual Studio build tools
- ollama not found → Ollama not installed / PATH not updated
- activate.ps1 blocked → PowerShell execution policy

NONE of these are coding mistakes.


8. CURRENT STATUS
-----------------
✔ Python installed
✔ Virtual environment created
✔ venv activation fixed
✔ Dependencies identified
✔ Ollama issue identified (pending install verification)

NEXT STEP:
----------
Confirm Ollama installation works:
> ollama --version

Then:
> python main.py

'''