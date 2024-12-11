# main_gui.py
import tkinter as tk
from tkinter import messagebox
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from database.db_setup import DATABASE_URL

# Importovanje GUI klasa
from gui.author_gui import AuthorGUI
from gui.book_gui import BookGUI
from gui.category_gui import CategoryGUI
from gui.member_gui import MemberGUI
from gui.publisher_gui import PublisherGUI
from gui.reservation_gui import ReservationGUI
from gui.transaction_gui import TransactionGUI

class MainGUI:
    def __init__(self, root, session: Session):
        self.root = root
        self.session = session
        self.root.title("Sistem za upravljanje bibliotekom")
        self.root.geometry("400x600")

        # Naslov
        title_label = tk.Label(root, text="Sistem za upravljanje bibliotekom", font=("Helvetica", 18, "bold"))
        title_label.pack(pady=20)

        # Dugmad za različite sekcije
        tk.Button(root, text="Upravljanje autorima", command=self.open_author_gui, width=30, height=2).pack(pady=5)
        tk.Button(root, text="Upravljanje knjigama", command=self.open_book_gui, width=30, height=2).pack(pady=5)
        tk.Button(root, text="Upravljanje kategorijama", command=self.open_category_gui, width=30, height=2).pack(pady=5)
        tk.Button(root, text="Upravljanje članovima", command=self.open_member_gui, width=30, height=2).pack(pady=5)
        tk.Button(root, text="Upravljanje izdavačima", command=self.open_publisher_gui, width=30, height=2).pack(pady=5)
        tk.Button(root, text="Upravljanje rezervacijama", command=self.open_reservation_gui, width=30, height=2).pack(pady=5)
        tk.Button(root, text="Upravljanje transakcijama", command=self.open_transaction_gui, width=30, height=2).pack(pady=5)
        tk.Button(root, text="Izlaz", command=self.root.quit, width=30, height=2).pack(pady=20)

    def open_author_gui(self):
        """Otvaranje GUI za upravljanje autorima."""
        AuthorGUI(self.root, self.session)

    def open_book_gui(self):
        """Otvaranje GUI za upravljanje knjigama."""
        BookGUI(self.root, self.session)

    def open_category_gui(self):
        """Otvaranje GUI za upravljanje kategorijama."""
        CategoryGUI(self.root, self.session)

    def open_member_gui(self):
        """Otvaranje GUI za upravljanje članovima."""
        member_window = tk.Toplevel(self.root)
        MemberGUI(member_window, self.session)

    def open_publisher_gui(self):
        """Otvaranje GUI za upravljanje izdavačima."""
        publisher_window = tk.Toplevel(self.root)
        PublisherGUI(publisher_window, self.session)

    def open_reservation_gui(self):
        """Otvaranje GUI za upravljanje rezervacijama."""
        reservation_window = tk.Toplevel(self.root)
        ReservationGUI(reservation_window, self.session)

    def open_transaction_gui(self):
        """Otvaranje GUI za upravljanje transakcijama."""
        transaction_window = tk.Toplevel(self.root)
        TransactionGUI(transaction_window, self.session)
