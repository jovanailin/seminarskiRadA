import tkinter as tk
from tkinter import messagebox
from services.book_service import (
    add_new_book,
    list_all_books_service,
    search_books_by_title_service,
    update_book_copies,
    remove_book,
    check_book_availability,
    get_total_book_count,
)
from sqlalchemy.orm import Session


class BookGUI:
    def __init__(self, root, session: Session):
        self.session = session
        self.window = tk.Toplevel(root)
        self.window.title("Upravljanje Knjigama")
        self.window.geometry("700x500")

        # Naslov
        title_label = tk.Label(self.window, text="Upravljanje Knjigama", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        # Lista za prikaz knjiga
        self.books_listbox = tk.Listbox(self.window, width=100, height=15)
        self.books_listbox.pack(pady=10)

        # Dugmad za funkcionalnosti
        tk.Button(self.window, text="Prikaži sve knjige", command=self.load_books, width=20).pack(pady=5)
        tk.Button(self.window, text="Dodaj novu knjigu", command=self.open_add_book_window, width=20).pack(pady=5)
        tk.Button(self.window, text="Pretraga po naslovu", command=self.open_search_book_window, width=20).pack(pady=5)
        tk.Button(self.window, text="Ažuriraj kopije", command=self.open_update_copies_window, width=20).pack(pady=5)
        tk.Button(self.window, text="Obriši knjigu", command=self.open_remove_book_window, width=20).pack(pady=5)
        tk.Button(self.window, text="Proveri dostupnost", command=self.open_check_availability_window, width=20).pack(pady=5)
        tk.Button(self.window, text="Ukupan broj knjiga", command=self.show_total_book_count, width=20).pack(pady=5)

        # Učitaj sve knjige pri pokretanju
        self.load_books()

    def load_books(self):
        self.books_listbox.delete(0, tk.END)
        books = list_all_books_service(self.session)
        for book in books:
            self.books_listbox.insert(
                tk.END, f"{book.BookID}: {book.Title} - Autor ID: {book.AuthorID} - Kopije: {book.AvailableCopies}"
            )

    def open_add_book_window(self):
        add_window = tk.Toplevel(self.window)
        add_window.title("Dodavanje nove knjige")
        add_window.geometry("400x400")

        tk.Label(add_window, text="Naslov:").pack()
        title_entry = tk.Entry(add_window)
        title_entry.pack()

        tk.Label(add_window, text="Autor ID:").pack()
        author_id_entry = tk.Entry(add_window)
        author_id_entry.pack()

        tk.Label(add_window, text="Izdavač ID:").pack()
        publisher_id_entry = tk.Entry(add_window)
        publisher_id_entry.pack()

        tk.Label(add_window, text="ISBN:").pack()
        isbn_entry = tk.Entry(add_window)
        isbn_entry.pack()

        tk.Label(add_window, text="Kategorija ID:").pack()
        category_id_entry = tk.Entry(add_window)
        category_id_entry.pack()

        tk.Label(add_window, text="Lokacija na polici:").pack()
        shelf_location_entry = tk.Entry(add_window)
        shelf_location_entry.pack()

        tk.Label(add_window, text="Ukupan broj kopija:").pack()
        total_copies_entry = tk.Entry(add_window)
        total_copies_entry.pack()

        tk.Label(add_window, text="Godina izdavanja:").pack()
        published_year_entry = tk.Entry(add_window)
        published_year_entry.pack()

        tk.Button(
            add_window,
            text="Dodaj knjigu",
            command=lambda: self.add_book(
                title_entry.get(),
                author_id_entry.get(),
                publisher_id_entry.get(),
                isbn_entry.get(),
                category_id_entry.get(),
                shelf_location_entry.get(),
                total_copies_entry.get(),
                published_year_entry.get(),
            ),
        ).pack(pady=10)

    def add_book(self, title, author_id, publisher_id, isbn, category_id, shelf_location, total_copies, published_year):
        try:
            author_id = int(author_id)
            publisher_id = int(publisher_id)
            category_id = int(category_id)
            total_copies = int(total_copies)
            published_year = int(published_year)

            new_book = add_new_book(
                self.session, title, author_id, publisher_id, isbn, category_id, shelf_location, total_copies, published_year
            )
            if new_book:
                messagebox.showinfo("Uspeh", f"Knjiga '{title}' je uspešno dodata.")
                self.load_books()
            else:
                messagebox.showwarning("Greška", "Dodavanje knjige nije uspelo.")
        except ValueError:
            messagebox.showwarning("Greška", "Unesite validne ID-ove i brojeve.")
        except Exception as e:
            messagebox.showerror("Greška", str(e))

    def open_search_book_window(self):
        search_window = tk.Toplevel(self.window)
        search_window.title("Pretraga knjiga")
        search_window.geometry("400x300")

        tk.Label(search_window, text="Unesite naslov:").pack()
        title_entry = tk.Entry(search_window)
        title_entry.pack()

        # Lista za prikaz rezultata
        search_results_listbox = tk.Listbox(search_window, width=50, height=10)
        search_results_listbox.pack(pady=10)

        # Povezivanje događaja
        title_entry.bind("<KeyRelease>", lambda event: self.update_search_results(title_entry.get(), search_results_listbox))

    def update_search_results(self, search_text, results_listbox):
        """Ažuriranje rezultata pretrage u realnom vremenu."""
        results_listbox.delete(0, tk.END)
        try:
            books = search_books_by_title_service(self.session, search_text)
            for book in books:
                results_listbox.insert(
                    tk.END, f"{book.BookID}: {book.Title} - Autor ID: {book.AuthorID}"
                )
            if not books:
                results_listbox.insert(tk.END, "Nema rezultata.")
        except Exception as e:
            messagebox.showerror("Greška", str(e))


    def search_books(self, title):
        self.books_listbox.delete(0, tk.END)
        try:
            books = search_books_by_title_service(self.session, title)
            for book in books:
                self.books_listbox.insert(
                    tk.END, f"{book.BookID}: {book.Title} - Autor ID: {book.AuthorID} - Kopije: {book.AvailableCopies}"
                )
            if not books:
                messagebox.showinfo("Rezultat pretrage", "Nijedna knjiga nije pronađena sa tim naslovom.")
        except Exception as e:
            messagebox.showerror("Greška", str(e))

    def open_update_copies_window(self):
        update_window = tk.Toplevel(self.window)
        update_window.title("Ažuriranje kopija")
        update_window.geometry("400x200")

        tk.Label(update_window, text="Unesite ID knjige:").pack()
        book_id_entry = tk.Entry(update_window)
        book_id_entry.pack()

        tk.Label(update_window, text="Unesite novi broj kopija:").pack()
        copies_entry = tk.Entry(update_window)
        copies_entry.pack()

        tk.Button(
            update_window, text="Ažuriraj", command=lambda: self.update_copies(book_id_entry.get(), copies_entry.get())
        ).pack(pady=10)

    def update_copies(self, book_id, available_copies):
        try:
            book_id = int(book_id)
            available_copies = int(available_copies)
            update_book_copies(self.session, book_id, available_copies)
            messagebox.showinfo("Uspeh", f"Broj kopija ažuriran za knjigu sa ID-jem {book_id}.")
            self.load_books()
        except ValueError:
            messagebox.showwarning("Greška", "ID knjige i broj kopija moraju biti brojevi.")
        except Exception as e:
            messagebox.showerror("Greška", str(e))

    def open_remove_book_window(self):
        remove_window = tk.Toplevel(self.window)
        remove_window.title("Brisanje knjige")
        remove_window.geometry("400x200")

        tk.Label(remove_window, text="Unesite ID knjige:").pack()
        book_id_entry = tk.Entry(remove_window)
        book_id_entry.pack()

        tk.Button(
            remove_window, text="Obriši", command=lambda: self.remove_book(book_id_entry.get())
        ).pack(pady=10)

    def remove_book(self, book_id):
        try:
            book_id = int(book_id)
            remove_book(self.session, book_id)
            messagebox.showinfo("Uspeh", f"Knjiga sa ID-jem {book_id} je obrisana.")
            self.load_books()
        except ValueError:
            messagebox.showwarning("Greška", "ID knjige mora biti broj.")
        except Exception as e:
            messagebox.showerror("Greška", str(e))

    def open_check_availability_window(self):
        availability_window = tk.Toplevel(self.window)
        availability_window.title("Provera dostupnosti")
        availability_window.geometry("400x200")

        tk.Label(availability_window, text="Unesite ID knjige:").pack()
        book_id_entry = tk.Entry(availability_window)
        book_id_entry.pack()

        tk.Button(
            availability_window,
            text="Proveri dostupnost",
            command=lambda: self.check_availability(book_id_entry.get()),
        ).pack(pady=10)

    def check_availability(self, book_id):
        try:
            book_id = int(book_id)
            available = check_book_availability(self.session, book_id)
            if available:
                messagebox.showinfo("Dostupnost", f"Knjiga sa ID-jem {book_id} je dostupna.")
            else:
                messagebox.showinfo("Dostupnost", f"Knjiga sa ID-jem {book_id} nije dostupna.")
        except ValueError:
            messagebox.showwarning("Greška", "ID knjige mora biti broj.")
        except Exception as e:
            messagebox.showerror("Greška", str(e))

    def show_total_book_count(self):
        try:
            count = get_total_book_count(self.session)
            messagebox.showinfo("Ukupan broj knjiga", f"Ukupan broj knjiga u biblioteci: {count}")
        except Exception as e:
            messagebox.showerror("Greška", str(e))
