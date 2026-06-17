import json
import os
import requests
import re

TODO_FILE = "todo.json"

if not os.path.exists(TODO_FILE):
    with open(TODO_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=2)


system_prompt = (
    "Esti un asistent care gestioneaza o lista de sarcini. "
    "Raspunde DOAR cu una dintre comenzile urmatoare, fara explicatii:\n"
    "- ADD:textul sarcinii (ex: ADD:cumpar lapte)\n"
    "- DELETE:numarul (ex: DELETE:2)\n"
    "- LIST\n"
    "- DONE:numarul (ex: DONE:1)"
)


def load_todos():
    with open(TODO_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_todos(todos):
    with open(TODO_FILE, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)


def show_todos(todos):
    if not todos:
        print("Lista de sarcini este goala.")
    else:
        for i, t in enumerate(todos, 1):
            status = "✓" if t.get("done") else "✗"
            print(f"{i}. [{status}] {t['text']}")


while True:
    user_input = input("> ").strip()
    if user_input.lower() in ("exit", "quit", "iesire"):
        break

    resp = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": os.getenv("OLLAMA_MODEL", "llama3.1"),
            "prompt": user_input,
            "system": system_prompt,
            "stream": False,
        },
    )
    reply = resp.json()["response"].strip()
    print(reply)

    todos = load_todos()

    if reply.startswith("ADD:"):
        text = reply[4:].strip()
        todos.append({"text": text, "done": False})
        save_todos(todos)
        print(f"Adaugat: {text}")

    elif reply.startswith("DELETE:"):
        match = re.search(r"\d+", reply)
        if match:
            idx = int(match.group()) - 1
            if 0 <= idx < len(todos):
                removed = todos.pop(idx)
                save_todos(todos)
                print(f"Sters: {removed['text']}")
            else:
                print("Numar invalid.")

    elif reply.startswith("DONE:"):
        match = re.search(r"\d+", reply)
        if match:
            idx = int(match.group()) - 1
            if 0 <= idx < len(todos):
                todos[idx]["done"] = True
                save_todos(todos)
                print(f"Marcat ca facut: {todos[idx]['text']}")
            else:
                print("Numar invalid.")

    elif reply == "LIST":
        show_todos(todos)

    else:
        print("Nu am inteles comanda. Incearca din nou.")
