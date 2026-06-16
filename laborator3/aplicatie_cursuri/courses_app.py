import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = "courses.json"


class CoursesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestionare Cursuri Universitare")
        self.root.geometry("750x550")
        self.root.resizable(False, False)

        self.courses = []
        self.load_data()

        self.create_widgets()
        self.refresh_table()

    # ------------------------------------------------------------------ DATA
    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                self.courses = json.load(f)
        else:
            self.courses = []

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.courses, f, indent=2, ensure_ascii=False)

    # ------------------------------------------------------------------ WIDGETS
    def create_widgets(self):
        # ---- Table
        frame_table = tk.LabelFrame(self.root, text="Cursuri salvate", padx=5, pady=5)
        frame_table.pack(fill="both", expand=True, padx=10, pady=(10, 5))

        columns = ("nume", "profesor", "credite")
        self.tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=10)
        self.tree.heading("nume", text="Nume curs")
        self.tree.heading("profesor", text="Profesor")
        self.tree.heading("credite", text="Credite")
        self.tree.column("nume", width=280)
        self.tree.column("profesor", width=220)
        self.tree.column("credite", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # ---- Form
        frame_form = tk.LabelFrame(self.root, text="Detalii curs", padx=10, pady=10)
        frame_form.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_form, text="Nume curs:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.entry_nume = tk.Entry(frame_form, width=35)
        self.entry_nume.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(frame_form, text="Profesor:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.entry_profesor = tk.Entry(frame_form, width=35)
        self.entry_profesor.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(frame_form, text="Credite:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.entry_credite = tk.Entry(frame_form, width=35)
        self.entry_credite.grid(row=2, column=1, padx=5, pady=2)

        # ---- Buttons
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack(fill="x", padx=10, pady=(0, 10))

        btn_adauga = tk.Button(frame_buttons, text="Adauga curs", command=self.add_course,
                               bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                               width=18, height=1)
        btn_adauga.pack(side="left", padx=5, pady=5)

        btn_modifica = tk.Button(frame_buttons, text="Modifica curs selectat",
                                 command=self.update_course,
                                 bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
                                 width=22, height=1)
        btn_modifica.pack(side="left", padx=5, pady=5)

        btn_sterge = tk.Button(frame_buttons, text="Sterge curs selectat",
                               command=self.delete_course,
                               bg="#f44336", fg="white", font=("Arial", 10, "bold"),
                               width=22, height=1)
        btn_sterge.pack(side="left", padx=5, pady=5)

    # ------------------------------------------------------------------ EVENTS
    def on_select(self, _event):
        selection = self.tree.selection()
        if not selection:
            return
        item = self.tree.item(selection[0])
        values = item["values"]
        self.entry_nume.delete(0, tk.END)
        self.entry_nume.insert(0, values[0])
        self.entry_profesor.delete(0, tk.END)
        self.entry_profesor.insert(0, values[1])
        self.entry_credite.delete(0, tk.END)
        self.entry_credite.insert(0, values[2])

    def clear_form(self):
        self.entry_nume.delete(0, tk.END)
        self.entry_profesor.delete(0, tk.END)
        self.entry_credite.delete(0, tk.END)
        self.tree.selection_remove(*self.tree.selection())

    # ------------------------------------------------------------------ CRUD
    def get_form_data(self):
        nume = self.entry_nume.get().strip()
        profesor = self.entry_profesor.get().strip()
        credite = self.entry_credite.get().strip()
        if not nume or not profesor or not credite:
            messagebox.showwarning("Campuri goale", "Completati toate campurile.")
            return None
        try:
            credite = int(credite)
        except ValueError:
            messagebox.showwarning("Eroare", "Credite trebuie sa fie un numar intreg.")
            return None
        return {"nume": nume, "profesor": profesor, "credite": credite}

    def add_course(self):
        data = self.get_form_data()
        if data is None:
            return
        self.courses.append(data)
        self.save_data()
        self.refresh_table()
        self.clear_form()
        messagebox.showinfo("Succes", "Curs adaugat cu succes.")

    def update_course(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Neselectat", "Selectati un curs din tabel.")
            return
        data = self.get_form_data()
        if data is None:
            return
        idx = self.tree.index(selection[0])
        self.courses[idx] = data
        self.save_data()
        self.refresh_table()
        self.clear_form()
        messagebox.showinfo("Succes", "Curs modificat cu succes.")

    def delete_course(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Neselectat", "Selectati un curs din tabel.")
            return
        if not messagebox.askyesno("Confirmare", "Sigur stergeti cursul selectat?"):
            return
        idx = self.tree.index(selection[0])
        del self.courses[idx]
        self.save_data()
        self.refresh_table()
        self.clear_form()
        messagebox.showinfo("Succes", "Curs sters cu succes.")

    # ------------------------------------------------------------------ REFRESH
    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for c in self.courses:
            self.tree.insert("", "end", values=(c["nume"], c["profesor"], c["credite"]))


if __name__ == "__main__":
    root = tk.Tk()
    app = CoursesApp(root)
    root.mainloop()
