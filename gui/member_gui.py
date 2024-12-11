import tkinter as tk
from tkinter import messagebox
from services.member_service import (
    add_new_member,
    find_member_by_id,
    find_members_by_name,
    list_all_members_service,
    update_member_info_with_validation,
    remove_member,
    get_total_member_count,
)
from sqlalchemy.orm import Session

class MemberGUI:
    def __init__(self, root, session: Session):
        self.session = session
        self.root = root
        self.root.title("Upravljanje Članovima")
        self.root.geometry("700x500")

        # Naslov
        title_label = tk.Label(self.root, text="Upravljanje Članovima", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        # Lista za prikaz članova
        self.members_listbox = tk.Listbox(self.root, width=100, height=15)
        self.members_listbox.pack(pady=10)

        # Dugmad za funkcionalnosti
        tk.Button(self.root, text="Prikaži sve članove", command=self.load_members, width=25).pack(pady=5)
        tk.Button(self.root, text="Dodaj novog člana", command=self.open_add_member_window, width=25).pack(pady=5)
        tk.Button(self.root, text="Pretraga po imenu", command=self.open_search_member_window, width=25).pack(pady=5)
        tk.Button(self.root, text="Ažuriraj podatke člana", command=self.open_update_member_window, width=25).pack(pady=5)
        tk.Button(self.root, text="Obriši člana", command=self.open_remove_member_window, width=25).pack(pady=5)

        # Učitaj sve članove pri pokretanju
        self.load_members()

    def load_members(self):
        """Prikaz svih članova u listbox-u."""
        self.members_listbox.delete(0, tk.END)
        try:
            members = list_all_members_service(self.session)
            for member in members:
                self.members_listbox.insert(
                    tk.END,
                    f"{member.MemberID}: {member.Name} - Kontakt: {member.ContactInfo} - Tip: {member.MembershipType}",
                )
            total_count = get_total_member_count(self.session)
            messagebox.showinfo("Ukupan broj članova", f"Ukupan broj članova: {total_count}")
        except Exception as e:
            messagebox.showerror("Greška", str(e))

    def open_add_member_window(self):
        """Otvaranje prozora za dodavanje novog člana."""
        add_window = tk.Toplevel(self.root)
        add_window.title("Dodavanje novog člana")
        add_window.geometry("400x400")

        # Polja za unos
        tk.Label(add_window, text="Ime:").pack()
        name_entry = tk.Entry(add_window)
        name_entry.pack()

        tk.Label(add_window, text="Adresa:").pack()
        address_entry = tk.Entry(add_window)
        address_entry.pack()

        tk.Label(add_window, text="Kontakt informacije:").pack()
        contact_info_entry = tk.Entry(add_window)
        contact_info_entry.pack()

        tk.Label(add_window, text="Datum članstva (YYYY-MM-DD):").pack()
        membership_date_entry = tk.Entry(add_window)
        membership_date_entry.pack()

        tk.Label(add_window, text="Tip članstva:").pack()
        membership_type_entry = tk.Entry(add_window)
        membership_type_entry.pack()

        # Dugme za dodavanje člana
        tk.Button(
            add_window,
            text="Dodaj člana",
            command=lambda: self.add_member(
                name_entry.get(),
                address_entry.get(),
                contact_info_entry.get(),
                membership_date_entry.get(),
                membership_type_entry.get(),
            ),
        ).pack(pady=10)

    def add_member(self, name, address, contact_info, membership_date, membership_type):
        """Dodavanje novog člana u bazu."""
        try:
            add_new_member(
                self.session, name, address, contact_info, membership_date, membership_type
            )
            messagebox.showinfo("Uspeh", f"Član '{name}' je uspešno dodat.")
            self.load_members()
        except Exception as e:
            messagebox.showerror("Greška", str(e))

    def open_search_member_window(self):
        """Otvaranje prozora za pretragu članova po imenu."""
        search_window = tk.Toplevel(self.root)
        search_window.title("Pretraga članova po imenu")
        search_window.geometry("400x200")

        tk.Label(search_window, text="Unesite ime:").pack()
        name_entry = tk.Entry(search_window)
        name_entry.pack()

        tk.Button(
            search_window,
            text="Pretraga",
            command=lambda: self.search_members(name_entry.get()),
        ).pack(pady=10)

    def search_members(self, name):
        """Pretraga članova po imenu."""
        self.members_listbox.delete(0, tk.END)
        try:
            members = find_members_by_name(self.session, name)
            for member in members:
                self.members_listbox.insert(
                    tk.END, f"{member.MemberID}: {member.Name} - Kontakt: {member.ContactInfo}"
                )
            if not members:
                messagebox.showinfo("Rezultat pretrage", "Nijedan član nije pronađen sa zadatim imenom.")
        except Exception as e:
            messagebox.showerror("Greška", str(e))

    def open_update_member_window(self):
        """Otvaranje prozora za ažuriranje informacija o članu."""
        update_window = tk.Toplevel(self.root)
        update_window.title("Ažuriranje podataka člana")
        update_window.geometry("400x300")

        tk.Label(update_window, text="Unesite ID člana:").pack()
        member_id_entry = tk.Entry(update_window)
        member_id_entry.pack()

        tk.Label(update_window, text="Novo ime (opciono):").pack()
        name_entry = tk.Entry(update_window)
        name_entry.pack()

        tk.Label(update_window, text="Nova adresa (opciono):").pack()
        address_entry = tk.Entry(update_window)
        address_entry.pack()

        tk.Label(update_window, text="Novi kontakt (opciono):").pack()
        contact_info_entry = tk.Entry(update_window)
        contact_info_entry.pack()

        tk.Button(
            update_window,
            text="Ažuriraj člana",
            command=lambda: self.update_member(
                member_id_entry.get(),
                name_entry.get(),
                address_entry.get(),
                contact_info_entry.get(),
            ),
        ).pack(pady=10)

    def update_member(self, member_id, name, address, contact_info):
        """Ažuriranje podataka člana."""
        try:
            kwargs = {
                k: v
                for k, v in [
                    ("Name", name),
                    ("Address", address),
                    ("ContactInfo", contact_info),
                ]
                if v
            }
            update_member_info_with_validation(self.session, int(member_id), **kwargs)
            messagebox.showinfo("Uspeh", f"Član sa ID-jem {member_id} je uspešno ažuriran.")
            self.load_members()
        except Exception as e:
            messagebox.showerror("Greška", str(e))

    def open_remove_member_window(self):
        """Otvaranje prozora za brisanje člana."""
        remove_window = tk.Toplevel(self.root)
        remove_window.title("Brisanje člana")
        remove_window.geometry("400x200")

        tk.Label(remove_window, text="Unesite ID člana:").pack()
        member_id_entry = tk.Entry(remove_window)
        member_id_entry.pack()

        tk.Button(
            remove_window,
            text="Obriši",
            command=lambda: self.remove_member(member_id_entry.get()),
        ).pack(pady=10)

    def remove_member(self, member_id):
        """Brisanje člana iz baze."""
        try:
            remove_member(self.session, int(member_id))
            messagebox.showinfo("Uspeh", f"Član sa ID-jem {member_id} je obrisan.")
            self.load_members()
        except Exception as e:
            messagebox.showerror("Greška", str(e))
