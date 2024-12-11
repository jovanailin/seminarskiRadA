import tkinter as tk
from tkinter import messagebox
from services.reservation_service import (
    create_reservation,
    find_reservation_by_id,
    list_all_active_reservations,
    list_all_reservations_service,
    update_reservation_status_service,
    cancel_reservation,
    validate_reservation_date,
)
from sqlalchemy.orm import Session
from datetime import datetime

class ReservationGUI:
    def __init__(self, root, session: Session):
        self.session = session
        self.root = root
        self.root.title("Upravljanje Rezervacijama")
        self.root.geometry("700x500")

        # Naslov
        title_label = tk.Label(root, text="Upravljanje Rezervacijama", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        # Lista za prikaz rezervacija
        self.reservations_listbox = tk.Listbox(root, width=100, height=15)
        self.reservations_listbox.pack(pady=10)

        # Dugmad za funkcionalnosti
        tk.Button(root, text="Prikaži sve rezervacije", command=self.load_all_reservations, width=25).pack(pady=5)
        tk.Button(root, text="Prikaži aktivne rezervacije", command=self.load_active_reservations, width=25).pack(pady=5)
        tk.Button(root, text="Dodaj novu rezervaciju", command=self.open_add_reservation_window, width=25).pack(pady=5)
        tk.Button(root, text="Pretraga po ID-u", command=self.open_search_reservation_window, width=25).pack(pady=5)
        tk.Button(root, text="Ažuriraj status rezervacije", command=self.open_update_reservation_window, width=25).pack(pady=5)
        tk.Button(root, text="Otkaži rezervaciju", command=self.open_cancel_reservation_window, width=25).pack(pady=5)

        # Učitaj sve rezervacije pri pokretanju
        self.load_all_reservations()

    def load_all_reservations(self):
        """Prikaz svih rezervacija u listbox-u."""
        self.reservations_listbox.delete(0, tk.END)
        try:
            reservations = list_all_reservations_service(self.session)
            for reservation in reservations:
                self.reservations_listbox.insert(
                    tk.END,
                    f"ID: {reservation.ReservationID}, ID Knjige: {reservation.BookID}, ID Člana: {reservation.MemberID}, Status: {reservation.Status}"
                )
        except Exception as e:
            messagebox.showerror("Greška", str(e))

    def load_active_reservations(self):
        """Prikaz aktivnih rezervacija u listbox-u."""
        self.reservations_listbox.delete(0, tk.END)
        try:
            reservations = list_all_active_reservations(self.session)
            for reservation in reservations:
                self.reservations_listbox.insert(
                    tk.END,
                    f"ID: {reservation.ReservationID}, ID Knjige: {reservation.BookID}, ID Člana: {reservation.MemberID}, Status: {reservation.Status}"
                )
        except Exception as e:
            messagebox.showerror("Greška", str(e))

    def open_add_reservation_window(self):
        """Otvaranje prozora za dodavanje nove rezervacije."""
        add_window = tk.Toplevel(self.root)
        add_window.title("Dodaj novu rezervaciju")
        add_window.geometry("400x300")

        # Polja za unos
        tk.Label(add_window, text="ID Knjige:").pack()
        book_id_entry = tk.Entry(add_window)
        book_id_entry.pack()

        tk.Label(add_window, text="ID Člana:").pack()
        member_id_entry = tk.Entry(add_window)
        member_id_entry.pack()

        tk.Label(add_window, text="Datum rezervacije (YYYY-MM-DD):").pack()
        reservation_date_entry = tk.Entry(add_window)
        reservation_date_entry.pack()

        # Dugme za kreiranje rezervacije
        tk.Button(
            add_window,
            text="Dodaj rezervaciju",
            command=lambda: self.add_reservation(
                book_id_entry.get(), member_id_entry.get(), reservation_date_entry.get()
            ),
        ).pack(pady=10)

    def add_reservation(self, book_id, member_id, reservation_date):
        """Dodavanje nove rezervacije u bazu."""
        try:
            reservation_date = datetime.strptime(reservation_date, "%Y-%m-%d").date()
            validate_reservation_date(reservation_date)
            create_reservation(self.session, int(book_id), int(member_id), reservation_date)
            messagebox.showinfo("Uspeh", "Rezervacija je uspešno kreirana.")
            self.load_all_reservations()
        except ValueError:
            messagebox.showerror("Greška", "Nepravilan format datuma. Koristite YYYY-MM-DD.")
        except Exception as e:
            messagebox.showerror("Greška", str(e))

    def open_search_reservation_window(self):
        """Otvaranje prozora za pretragu rezervacije po ID-u."""
        search_window = tk.Toplevel(self.root)
        search_window.title("Pretraga rezervacije po ID-u")
        search_window.geometry("400x200")

        tk.Label(search_window, text="Unesite ID rezervacije:").pack()
        reservation_id_entry = tk.Entry(search_window)
        reservation_id_entry.pack()

        tk.Button(
            search_window,
            text="Pretraga",
            command=lambda: self.search_reservation_by_id(reservation_id_entry.get()),
        ).pack(pady=10)

    def search_reservation_by_id(self, reservation_id):
        """Pretraga rezervacije po ID-u."""
        self.reservations_listbox.delete(0, tk.END)
        try:
            reservation = find_reservation_by_id(self.session, int(reservation_id))
            if reservation:
                self.reservations_listbox.insert(
                    tk.END,
                    f"ID: {reservation.ReservationID}, ID Knjige: {reservation.BookID}, ID Člana: {reservation.MemberID}, Status: {reservation.Status}"
                )
            else:
                messagebox.showinfo("Rezultat pretrage", "Rezervacija nije pronađena.")
        except ValueError:
            messagebox.showerror("Greška", "ID mora biti broj.")
        except Exception as e:
            messagebox.showerror("Greška", str(e))

    def open_update_reservation_window(self):
        """Otvaranje prozora za ažuriranje statusa rezervacije."""
        update_window = tk.Toplevel(self.root)
        update_window.title("Ažuriranje statusa rezervacije")
        update_window.geometry("400x200")

        tk.Label(update_window, text="Unesite ID rezervacije:").pack()
        reservation_id_entry = tk.Entry(update_window)
        reservation_id_entry.pack()

        tk.Label(update_window, text="Unesite novi status:").pack()
        status_entry = tk.Entry(update_window)
        status_entry.pack()

        tk.Button(
            update_window,
            text="Ažuriraj",
            command=lambda: self.update_reservation_status(
                reservation_id_entry.get(), status_entry.get()
            ),
        ).pack(pady=10)

    def update_reservation_status(self, reservation_id, new_status):
        """Ažuriranje statusa rezervacije."""
        try:
            update_reservation_status_service(self.session, int(reservation_id), new_status)
            messagebox.showinfo("Uspeh", "Status je uspešno ažuriran.")
            self.load_all_reservations()
        except ValueError:
            messagebox.showerror("Greška", "ID mora biti broj.")
        except Exception as e:
            messagebox.showerror("Greška", str(e))

    def open_cancel_reservation_window(self):
        """Otvaranje prozora za otkazivanje rezervacije."""
        cancel_window = tk.Toplevel(self.root)
        cancel_window.title("Otkaži rezervaciju")
        cancel_window.geometry("400x200")

        tk.Label(cancel_window, text="Unesite ID rezervacije:").pack()
        reservation_id_entry = tk.Entry(cancel_window)
        reservation_id_entry.pack()

        tk.Button(
            cancel_window,
            text="Otkaži rezervaciju",
            command=lambda: self.cancel_reservation(reservation_id_entry.get()),
        ).pack(pady=10)

    def cancel_reservation(self, reservation_id):
        """Otkazivanje rezervacije."""
        try:
            cancel_reservation(self.session, int(reservation_id))
            messagebox.showinfo("Uspeh", "Rezervacija je otkazana.")
            self.load_all_reservations()
        except ValueError:
            messagebox.showerror("Greška", "ID mora biti broj.")
        except Exception as e:
            messagebox.showerror("Greška", str(e))
