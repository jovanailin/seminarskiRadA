# 📚 Sistem za upravljanje bibliotekom

Ovaj studentski projekat, realizovan u okviru predmeta Seminarski rad A na Prirodno-matematičkom fakultetu, Univerziteta u Novom Sadu, implementira aplikaciju za upravljanje bibliotekom. Osnovni cilj projekta je demonstracija ORM pristupa u Pythonu.

## 🛠️ Funkcionalnosti

- Dodavanje, ažuriranje, pretraga i brisanje knjiga, autora, članova, izdavača, rezervacija i transakcija.
- Prikaz svih entiteta u biblioteci putem grafičkog korisničkog interfejsa.
- Intuitivan dizajn korisničkog interfejsa koji omogućava lako upravljanje podacima.

## ⚙️ Tehnologije

- **Python**: Glavni programski jezik.
- **Tkinter**: Za grafički korisnički interfejs.
- **SQLAlchemy**: Za rad sa bazom podataka i ORM.
- **PostgreSQL**: Baza podataka korišćena u projektu.

## 📂 Struktura Projekta
 
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

## 💻 Kako Pokrenuti Projekat

### 1. Kloniranje Repozitorijuma
```bash
git clone https://github.com/username/library-management-system.git
cd library-management-system
```

## 💻 Instalacija Zavisnosti
Preporučuje se korišćenje virtuelnog okruženja:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 💻 Pokretanje Aplikacije
Pokrenite aplikaciju iz glavnog fajla:
```bash
python app.py
```
