import os
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama" # Ollama are nevoie de orice text aici ca să nu dea eroare
)

oras = input("Introdu numele orasului: ")

try:
    response = client.chat.completions.create(
        model="llama3",
        messages=[
            {"role": "user", "content": f"Cum este vremea in {oras} acum?"}
        ],
        temperature=0.7,
    )
    
    print("\n--- Raspuns de la AI (Model Simplu) ---")
    print(response.choices[0].message.content)

except Exception as e:
    print(f"A aparut o eroare: {e}")