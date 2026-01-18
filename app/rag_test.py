from app.rag_engine import build_rag_chain

qa = build_rag_chain()

question = (
    "Why is metro considered more environmentally friendly "
    "than private cars for daily commuting?"
)

answer = qa.run(question)

print("\nAI RESPONSE:\n")
print(answer)
