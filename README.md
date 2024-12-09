# Sistem za upravljanje bibliotekom

Ovaj projekat implementira aplikaciju za upravljanje bibliotekom koristeći Python, Tkinter za grafički interfejs i SQLAlchemy za upravljanje bazom podataka.

## Funkcionalnosti

- Dodavanje, ažuriranje, pretraga i brisanje knjiga, autora, članova, izdavača, rezervacija i transakcija.
- Prikaz svih entiteta u biblioteci putem grafičkog korisničkog interfejsa.
- Intuitivan dizajn korisničkog interfejsa koji omogućava lako upravljanje podacima.

## Tehnologije

- **Python**: Glavni programski jezik.
- **Tkinter**: Za grafički korisnički interfejs.
- **SQLAlchemy**: Za rad sa bazom podataka i ORM.
- **SQLite**: Baza podataka korišćena u projektu.

## Struktura Projekta

```plaintext
├── database/
│   ├── db_setup.py          # Postavka baze podataka
│   ├── db_operations.py     # CRUD operacije za bazu podataka
│   └── models.py            # SQLAlchemy modeli
├── gui/
│   ├── main_gui.py          # Glavni grafički interfejs
│   ├── book_gui.py          # GUI za knjige
│   ├── author_gui.py        # GUI za autore
│   ├── category_gui.py      # GUI za kategorije
│   ├── publisher_gui.py     # GUI za izdavače
│   ├── member_gui.py        # GUI za članove
│   ├── reservation_gui.py   # GUI za rezervacije
│   └── transaction_gui.py   # GUI za transakcije
├── services/
│   ├── book_service.py      # Servisi za knjige
│   ├── author_service.py    # Servisi za autore
│   ├── category_service.py  # Servisi za kategorije
│   ├── publisher_service.py # Servisi za izdavače
│   ├── member_service.py    # Servisi za članove
│   ├── reservation_service.py # Servisi za rezervacije
│   └── transaction_service.py # Servisi za transakcije
├── app.py                   # Ulazna tačka aplikacije
└── requirements.txt         # Lista potrebnih biblioteka
```

