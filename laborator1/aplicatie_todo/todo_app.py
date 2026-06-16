import json
import os

DATA_FILE = "tasks.json"


def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)


def add_task(tasks):
    title = input("Introdu titlul sarcinii: ").strip()
    if not title:
        print("Titlul nu poate fi gol.")
        return
    tasks.append({"id": len(tasks) + 1, "title": title, "done": False})
    print(f"Sarcina \"{title}\" a fost adaugata.")


def list_tasks(tasks):
    if not tasks:
        print("Nu exista sarcini.")
        return
    for t in tasks:
        status = "\u2713" if t["done"] else "\u2717"
        print(f"[{status}] {t['id']}. {t['title']}")


def delete_task(tasks):
    list_tasks(tasks)
    try:
        tid = int(input("ID-ul sarcinii de sters: "))
    except ValueError:
        print("ID invalid.")
        return
    for i, t in enumerate(tasks):
        if t["id"] == tid:
            del tasks[i]
            print("Sarcina a fost stearsa.")
            return
    print("ID inexistent.")


def mark_done(tasks):
    list_tasks(tasks)
    try:
        tid = int(input("ID-ul sarcinii de marcat ca rezolvata: "))
    except ValueError:
        print("ID invalid.")
        return
    for t in tasks:
        if t["id"] == tid:
            t["done"] = True
            print("Sarcina a fost marcata ca rezolvata.")
            return
    print("ID inexistent.")


def main():
    tasks = load_tasks()
    while True:
        print("\n--- TODO LIST ---")
        print("1. Adauga sarcina")
        print("2. Vezi toate sarcinile")
        print("3. Sterge sarcina")
        print("4. Marcheaza ca rezolvata")
        print("5. Iesire")
        opt = input("Alege o optiune: ").strip()
        if opt == "1":
            add_task(tasks)
        elif opt == "2":
            list_tasks(tasks)
        elif opt == "3":
            delete_task(tasks)
        elif opt == "4":
            mark_done(tasks)
        elif opt == "5":
            save_tasks(tasks)
            print("La revedere!")
            break
        else:
            print("Optiune invalida.")


if __name__ == "__main__":
    main()
