import tkinter as tk
from tkinter import messagebox
from services.author_service import (
    add_new_author,
    find_author_by_id,
    find_author_by_name,
    list_all_authors_service,
    update_author_with_validation,
    remove_author,
    get_book_count_by_author_service,
    get_authors_with_books_service,
)
from sqlalchemy.orm import Session


class AuthorGUI:
    def __init__(self, root, session: Session):
        self.session = session
        self.window = tk.Toplevel(root)
        self.window.title("Upravljanje autorima")
        self.window.geometry("700x500")

        # Naslov
        title_label = tk.Label(self.window, text="Upravljanje Autorima", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        # Lista za prikaz autora
        self.authors_listbox = tk.Listbox(self.window, width=100, height=15)
        self.authors_listbox.pack(pady=10)

        # Dugmad za funkcionalnosti
        tk.Button(self.window, text="Prikaži sve autore", command=self.load_authors, width=20).pack(pady=5)
        tk.Button(self.window, text="Dodaj novog autora", command=self.open_add_author_window, width=20).pack(pady=5)
        tk.Button(self.window, text="Pretraga po imenu", command=self.open_search_author_window, width=20).pack(pady=5)
        tk.Button(self.window, text="Ažuriraj podatke", command=self.open_update_author_window, width=20).pack(pady=5)
        tk.Button(self.window, text="Obriši autora", command=self.open_remove_author_window, width=20).pack(pady=5)
        tk.Button(self.window, text="Knjige po autoru", command=self.open_book_count_by_author_window, width=20).pack(pady=5)
        tk.Button(self.window, text="Autori i njihove knjige", command=self.show_authors_with_books, width=20).pack(pady=5)

        # Učitaj sve autore pri pokretanju
        self.load_authors()

    def load_authors(self):
        self.authors_listbox.delete(0, tk.END)
        try:
            authors = list_all_authors_service(self.session)
            for author in authors:
                self.authors_listbox.insert(
                    tk.END, f"{author.AuthorID}: {author.Name} - Nacionalnost: {author.Nationality}"
                )
        except Exception as e:
            messagebox.showerror("Greška", str(e))

    def open_add_author_window(self):
        add_window = tk.Toplevel(self.window)
        add_window.title("Dodavanje autora")
        add_window.geometry("400x400")

        tk.Label(add_window, text="Ime:").pack()
        name_entry = tk.Entry(add_window)
        name_entry.pack()

        tk.Label(add_window, text="Biografija:").pack()
        bio_text = tk.Text(add_window, height=15, width=40)
        bio_text.pack()

        tk.Label(add_window, text="Nacionalnost:").pack()
        nationality_entry = tk.Entry(add_window)
        nationality_entry.pack()

        tk.Button(
            add_window,
            text="Dodaj autora",
            command=lambda: self.add_author(name_entry.get(), bio_text.get("1.0", tk.END).strip(), nationality_entry.get()),
        ).pack(pady=10)


    def add_author(self, name, bio, nationality):
        try:
            add_new_author(name, bio, nationality, self.session)
            messagebox.showinfo("Uspeh", f"Autor '{name}' je uspešno dodat.")
            self.load_authors()
        except Exception as e:
            messagebox.showerror("Greška", str(e))

    def open_search_author_window(self):
        search_window = tk.Toplevel(self.window)
        search_window.title("Pretraga autora")
        search_window.geometry("400x400")

        tk.Label(search_window, text="Unesite ime:").pack()

        # Entry za unos imena
        name_entry = tk.Entry(search_window)
        name_entry.pack()
        name_entry.bind("<KeyRelease>", lambda event: self.search_author_by_name_real_time(name_entry.get(), result_listbox))

        # Listbox za prikaz rezultata pretrage
        result_listbox = tk.Listbox(search_window, width=50, height=15)
        result_listbox.pack(pady=10)

    def search_author_by_name_real_time(self, name, listbox):
        listbox.delete(0, tk.END)
        try:
            authors = find_author_by_name(name, self.session)
            for author in authors:
                listbox.insert(
                    tk.END, f"{author.AuthorID}: {author.Name} - Nacionalnost: {author.Nationality}"
                )
            if not authors:
                listbox.insert(tk.END, "Nema rezultata.")
        except Exception as e:
            messagebox.showerror("Greška", str(e))


    def search_author_by_name(self, name):
        self.authors_listbox.delete(0, tk.END)
        try:
            authors = find_author_by_name(name, self.session)
            for author in authors:
                self.authors_listbox.insert(
                    tk.END, f"{author.AuthorID}: {author.Name} - Nacionalnost: {author.Nationality}"
                )
            if not authors:
                messagebox.showinfo("Rezultat pretrage", "Nijedan autor nije pronađen.")
        except Exception as e:
            messagebox.showerror("Greška", str(e))

    def open_update_author_window(self):
        update_window = tk.Toplevel(self.window)
        update_window.title("Ažuriranje autora")
        update_window.geometry("400x300")

        tk.Label(update_window, text="Unesite ID autora:").pack()
        author_id_entry = tk.Entry(update_window)
        author_id_entry.pack()

        tk.Label(update_window, text="Novo ime (opciono):").pack()
        name_entry = tk.Entry(update_window)
        name_entry.pack()

        tk.Label(update_window, text="Nova biografija (opciono):").pack()
        bio_entry = tk.Text(update_window, height=5, width=40)
        bio_entry.pack()

        tk.Label(update_window, text="Nova nacionalnost (opciono):").pack()
        nationality_entry = tk.Entry(update_window)
        nationality_entry.pack()

        tk.Button(
            update_window,
            text="Ažuriraj autora",
            command=lambda: self.update_author(
                author_id_entry.get(),
                name_entry.get(),
                bio_entry.get("1.0", tk.END).strip(),
                nationality_entry.get(),
            ),
        ).pack(pady=10)

    def update_author(self, author_id, name, bio, nationality):
        try:
            kwargs = {k: v for k, v in [("Name", name), ("Bio", bio), ("Nationality", nationality)] if v}
            update_author_with_validation(author_id, self.session, **kwargs)
            messagebox.showinfo("Uspeh", f"Autor sa ID-jem {author_id} je uspešno ažuriran.")
            self.load_authors()
        except Exception as e:
            messagebox.showerror("Greška", str(e))

    def open_remove_author_window(self):
        remove_window = tk.Toplevel(self.window)
        remove_window.title("Brisanje autora")
        remove_window.geometry("400x200")

        tk.Label(remove_window, text="Unesite ID autora:").pack()
        author_id_entry = tk.Entry(remove_window)
        author_id_entry.pack()

        tk.Button(
            remove_window, text="Obriši", command=lambda: self.remove_author(author_id_entry.get())
        ).pack(pady=10)

    def remove_author(self, author_id):
        try:
            remove_author(author_id, self.session)
            messagebox.showinfo("Uspeh", f"Autor sa ID-jem {author_id} je obrisan.")
            self.load_authors()
        except Exception as e:
            messagebox.showerror("Greška", str(e))

    def open_book_count_by_author_window(self):
        count_window = tk.Toplevel(self.window)
        count_window.title("Broj knjiga po autoru")
        count_window.geometry("400x200")

        tk.Label(count_window, text="Unesite ID autora:").pack()
        author_id_entry = tk.Entry(count_window)
        author_id_entry.pack()

        tk.Button(
            count_window, text="Prikaži broj knjiga", command=lambda: self.get_book_count_by_author(author_id_entry.get())
        ).pack(pady=10)

    def get_book_count_by_author(self, author_id):
        try:
            count = get_book_count_by_author_service(author_id, self.session)
            messagebox.showinfo("Broj knjiga", f"Autor sa ID-jem {author_id} je napisao {count} knjiga.")
        except Exception as e:
            messagebox.showerror("Greška", str(e))

    def show_authors_with_books(self):
        try:
            authors = get_authors_with_books_service(self.session)
            self.authors_listbox.delete(0, tk.END)
            for author in authors:
                self.authors_listbox.insert(
                    tk.END, f"{author.AuthorID}: {author.Name} - Knjige: {[book.Title for book in author.books]}"
                )
        except Exception as e:
            messagebox.showerror("Greška", str(e))
