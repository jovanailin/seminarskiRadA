import tkinter as tk
from tkinter import messagebox
from services.transaction_service import (
    borrow_book,
    return_book,
    list_all_transactions_service,
    list_active_borrowed_books,
    list_member_transactions,
    list_overdue_transactions,
    list_transactions_by_status,
)
from sqlalchemy.orm import Session

class TransactionGUI:
    def __init__(self, root, session: Session):
        self.session = session
        self.root = root
        self.root.title("Upravljanje Transakcijama")
        self.root.geometry("800x600")

        # Naslov
        title_label = tk.Label(root, text="Upravljanje Transakcijama", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        # Lista za prikaz transakcija
        self.transactions_listbox = tk.Listbox(root, width=100, height=15)
        self.transactions_listbox.pack(pady=10)

        # Dugmad za funkcionalnosti
        tk.Button(root, text="Prikaži sve transakcije", command=self.load_transactions, width=30).pack(pady=5)
        tk.Button(root, text="Iznajmi knjigu", command=self.open_borrow_book_window, width=30).pack(pady=5)
        tk.Button(root, text="Vrati knjigu", command=self.open_return_book_window, width=30).pack(pady=5)
        tk.Button(root, text="Prikaži aktivne knjige", command=self.load_active_borrowed_books, width=30).pack(pady=5)
        tk.Button(root, text="Prikaži zakašnjele transakcije", command=self.load_overdue_transactions, width=30).pack(pady=5)
        tk.Button(root, text="Prikaži transakcije po članu", command=self.open_list_member_transactions_window, width=30).pack(pady=5)
        tk.Button(root, text="Prikaži transakcije po statusu", command=self.open_list_status_transactions_window, width=30).pack(pady=5)

        # Učitaj sve transakcije pri pokretanju
        self.load_transactions()

    def load_transactions(self):
        """Prikaz svih transakcija u listbox-u."""
        self.transactions_listbox.delete(0, tk.END)
        try:
            transactions = list_all_transactions_service(self.session)
            for transaction in transactions:
                self.transactions_listbox.insert(
                    tk.END,
                    f"ID Transakcije: {transaction.TransactionID} - ID Knjige: {transaction.BookID} - ID Člana: {transaction.MemberID} - Status: {transaction.Status}"
                )
        except Exception as e:
            messagebox.showerror("Greška", str(e))

    def open_borrow_book_window(self):
        """Otvaranje prozora za iznajmljivanje knjige."""
        borrow_window = tk.Toplevel(self.root)
        borrow_window.title("Iznajmi Knjigu")
        borrow_window.geometry("400x300")

        # Polja za unos
        tk.Label(borrow_window, text="ID Knjige:").pack()
        book_id_entry = tk.Entry(borrow_window)
        book_id_entry.pack()

        tk.Label(borrow_window, text="ID Člana:").pack()
        member_id_entry = tk.Entry(borrow_window)
        member_id_entry.pack()

        tk.Label(borrow_window, text="Datum iznajmljivanja (YYYY-MM-DD):").pack()
        borrow_date_entry = tk.Entry(borrow_window)
        borrow_date_entry.pack()

        tk.Label(borrow_window, text="Rok za vraćanje (YYYY-MM-DD):").pack()
        due_date_entry = tk.Entry(borrow_window)
        due_date_entry.pack()

        # Dugme za iznajmljivanje knjige
        tk.Button(
            borrow_window,
            text="Iznajmi Knjigu",
            command=lambda: self.borrow_book(
                book_id_entry.get(),
                member_id_entry.get(),
                borrow_date_entry.get(),
                due_date_entry.get(),
            ),
        ).pack(pady=10)

    def borrow_book(self, book_id, member_id, borrow_date, due_date):
        """Iznajmljivanje knjige."""
        try:
            transaction = borrow_book(self.session, int(book_id), int(member_id), borrow_date, due_date)
            if transaction:
                messagebox.showinfo("Uspeh", f"Knjiga ID {book_id} uspešno iznajmljena.")
                self.load_transactions()
            else:
                messagebox.showwarning("Greška", "Iznajmljivanje nije uspelo. Proverite dostupnost ili unos.")
        except ValueError:
            messagebox.showwarning("Greška", "ID Knjige i ID Člana moraju biti brojevi.")
        except Exception as e:
            messagebox.showerror("Greška", str(e))

    def open_return_book_window(self):
        """Otvaranje prozora za vraćanje knjige."""
        return_window = tk.Toplevel(self.root)
        return_window.title("Vrati Knjigu")
        return_window.geometry("400x200")

        tk.Label(return_window, text="ID Transakcije:").pack()
        transaction_id_entry = tk.Entry(return_window)
        transaction_id_entry.pack()

        tk.Label(return_window, text="Datum vraćanja (YYYY-MM-DD):").pack()
        return_date_entry = tk.Entry(return_window)
        return_date_entry.pack()

        tk.Button(
            return_window,
            text="Vrati Knjigu",
            command=lambda: self.return_book(transaction_id_entry.get(), return_date_entry.get()),
        ).pack(pady=10)

    def return_book(self, transaction_id, return_date):
        """Vraćanje knjige."""
        try:
            transaction = return_book(self.session, int(transaction_id), return_date)
            if transaction:
                messagebox.showinfo("Uspeh", f"Transakcija ID {transaction_id} uspešno završena.")
                self.load_transactions()
            else:
                messagebox.showwarning("Greška", "Vraćanje nije uspelo. Proverite ID transakcije ili unos.")
        except ValueError:
            messagebox.showwarning("Greška", "ID Transakcije mora biti broj.")
        except Exception as e:
            messagebox.showerror("Greška", str(e))

    def load_active_borrowed_books(self):
        """Prikaz trenutno iznajmljenih knjiga."""
        self.transactions_listbox.delete(0, tk.END)
        try:
            transactions = list_active_borrowed_books(self.session)
            for transaction in transactions:
                self.transactions_listbox.insert(
                    tk.END,
                    f"ID Transakcije: {transaction.TransactionID} - ID Knjige: {transaction.BookID} - ID Člana: {transaction.MemberID} - Status: {transaction.Status}"
                )
            if not transactions:
                messagebox.showinfo("Informacija", "Nema trenutno iznajmljenih knjiga.")
        except Exception as e:
            messagebox.showerror("Greška", str(e))

    def load_overdue_transactions(self):
        """Prikaz zakašnjelih transakcija."""
        self.transactions_listbox.delete(0, tk.END)
        try:
            transactions = list_overdue_transactions(self.session)
            for transaction in transactions:
                self.transactions_listbox.insert(
                    tk.END,
                    f"ID Transakcije: {transaction.TransactionID} - ID Knjige: {transaction.BookID} - Rok: {transaction.DueDate}"
                )
            if not transactions:
                messagebox.showinfo("Informacija", "Nema zakašnjelih transakcija.")
        except Exception as e:
            messagebox.showerror("Greška", str(e))
