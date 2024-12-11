import tkinter as tk
from tkinter import messagebox
from services.category_service import (
    add_new_category,
    find_category_by_id,
    search_category_by_name,
    list_all_categories_with_count,
    update_category,
    remove_category,
)
from sqlalchemy.orm import Session


class CategoryGUI:
    def __init__(self, root, session: Session):
        self.session = session
        self.window = tk.Toplevel(root)
        self.window.title("Upravljanje Kategorijama")
        self.window.geometry("700x500")

        # Naslov
        title_label = tk.Label(self.window, text="Upravljanje Kategorijama", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        # Lista za prikaz kategorija
        self.categories_listbox = tk.Listbox(self.window, width=100, height=15)
        self.categories_listbox.pack(pady=10)

        # Dugmad za funkcionalnosti
        tk.Button(self.window, text="Prikaži sve kategorije", command=self.load_categories, width=25).pack(pady=5)
        tk.Button(self.window, text="Dodaj novu kategoriju", command=self.open_add_category_window, width=25).pack(pady=5)
        tk.Button(self.window, text="Pretraga po nazivu", command=self.open_search_category_window, width=25).pack(pady=5)
        tk.Button(self.window, text="Ažuriraj kategoriju", command=self.open_update_category_window, width=25).pack(pady=5)
        tk.Button(self.window, text="Obriši kategoriju", command=self.open_remove_category_window, width=25).pack(pady=5)

        # Učitaj sve kategorije pri pokretanju
        self.load_categories()

    def load_categories(self):
        self.categories_listbox.delete(0, tk.END)
        try:
            result = list_all_categories_with_count(self.session)
            categories = result["kategorije"]
            total_count = result["ukupan_broj"]

            for category in categories:
                self.categories_listbox.insert(
                    tk.END, f"{category.CategoryID}: {category.CategoryName} - Opis: {category.Description}"
                )
            messagebox.showinfo("Ukupan broj kategorija", f"Ukupan broj kategorija: {total_count}")
        except Exception as e:
            messagebox.showerror("Greška", str(e))

    def open_add_category_window(self):
        add_window = tk.Toplevel(self.window)
        add_window.title("Dodavanje nove kategorije")
        add_window.geometry("400x300")

        tk.Label(add_window, text="Naziv kategorije:").pack()
        name_entry = tk.Entry(add_window)
        name_entry.pack()

        tk.Label(add_window, text="Opis:").pack()
        description_entry = tk.Entry(add_window)
        description_entry.pack()

        tk.Button(
            add_window,
            text="Dodaj kategoriju",
            command=lambda: self.add_category(name_entry.get(), description_entry.get()),
        ).pack(pady=10)

    def add_category(self, name, description):
        try:
            add_new_category(self.session, name, description)
            messagebox.showinfo("Uspeh", f"Kategorija '{name}' je uspešno dodata.")
            self.load_categories()
        except Exception as e:
            messagebox.showerror("Greška", str(e))

    def open_search_category_window(self):
        search_window = tk.Toplevel(self.window)
        search_window.title("Pretraga kategorije")
        search_window.geometry("400x200")

        tk.Label(search_window, text="Unesite naziv kategorije:").pack()
        name_entry = tk.Entry(search_window)
        name_entry.pack()

        tk.Button(
            search_window, text="Pretraga", command=lambda: self.search_category_by_name(name_entry.get())
        ).pack(pady=10)

    def search_category_by_name(self, name):
        self.categories_listbox.delete(0, tk.END)
        try:
            categories = search_category_by_name(self.session, name)
            for category in categories:
                self.categories_listbox.insert(
                    tk.END, f"{category.CategoryID}: {category.CategoryName} - Opis: {category.Description}"
                )
            if not categories:
                messagebox.showinfo("Rezultat pretrage", "Nijedna kategorija nije pronađena sa zadatim nazivom.")
        except Exception as e:
            messagebox.showerror("Greška", str(e))

    def open_update_category_window(self):
        update_window = tk.Toplevel(self.window)
        update_window.title("Ažuriranje kategorije")
        update_window.geometry("400x300")

        tk.Label(update_window, text="Unesite ID kategorije:").pack()
        category_id_entry = tk.Entry(update_window)
        category_id_entry.pack()

        tk.Label(update_window, text="Novi naziv (opciono):").pack()
        name_entry = tk.Entry(update_window)
        name_entry.pack()

        tk.Label(update_window, text="Novi opis (opciono):").pack()
        description_entry = tk.Entry(update_window)
        description_entry.pack()

        tk.Button(
            update_window,
            text="Ažuriraj kategoriju",
            command=lambda: self.update_category(
                category_id_entry.get(), name_entry.get(), description_entry.get()
            ),
        ).pack(pady=10)

    def update_category(self, category_id, name, description):
        try:
            kwargs = {k: v for k, v in [("CategoryName", name), ("Description", description)] if v}
            update_category(self.session, category_id, **kwargs)
            messagebox.showinfo("Uspeh", f"Kategorija sa ID-jem {category_id} je uspešno ažurirana.")
            self.load_categories()
        except Exception as e:
            messagebox.showerror("Greška", str(e))

    def open_remove_category_window(self):
        remove_window = tk.Toplevel(self.window)
        remove_window.title("Brisanje kategorije")
        remove_window.geometry("400x200")

        tk.Label(remove_window, text="Unesite ID kategorije:").pack()
        category_id_entry = tk.Entry(remove_window)
        category_id_entry.pack()

        tk.Button(
            remove_window, text="Obriši", command=lambda: self.remove_category(category_id_entry.get())
        ).pack(pady=10)

    def remove_category(self, category_id):
        try:
            remove_category(self.session, category_id)
            messagebox.showinfo("Uspeh", f"Kategorija sa ID-jem {category_id} je obrisana.")
            self.load_categories()
        except Exception as e:
            messagebox.showerror("Greška", str(e))
