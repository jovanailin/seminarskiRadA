# Seminarski Rad A
## Python i ORM pristup

### Sistem za Upravljanje Bibliotekom

---

## 📚 Sistem za Upravljanje Bibliotekom

Ovo je studebtsju projekat u sklopu predmeta "Seminarski rad A" na Prirodno-matematičkom fakultetu, univerziteta u Novom Sadu. Razvijena je desktop aplikacija za upravljanje bibliotekom, korišćenjem alata: **Python**, **Tkinter** i **SQLAlchemy**. Omogućava korisnicima da upravljaju knjigama, autorima, izdavačima, kategorijama, članovima, rezervacijama i transakcijama kroz intuitivan grafički interfejs.

---

## 🛠️ Funkcionalnosti

- **Upravljanje knjigama**: Dodavanje, ažuriranje, pretraga, brisanje i proveravanje dostupnosti knjiga.
- **Upravljanje autorima**: Dodavanje autora, pretraga po imenu, ažuriranje podataka i brisanje autora.
- **Upravljanje izdavačima**: Dodavanje izdavača, pretraga, ažuriranje i brisanje.
- **Upravljanje kategorijama**: Dodavanje, ažuriranje i pretraga kategorija.
- **Upravljanje članovima**: Evidencija članova, pretraga, dodavanje i ažuriranje podataka.
- **Rezervacije i transakcije**: Upravljanje rezervacijama knjiga i evidencija zaduženja i vraćanja knjiga.
- **Pregled podataka**: Prikaz svih unetih podataka uz mogućnost sortiranja i filtriranja.

---

## 📂 Struktura Projekta
├── database/ │ ├── db_setup.py # Postavka baze podataka │ ├── db_operations.py # CRUD operacije za bazu podataka │ └── models.py # SQLAlchemy modeli ├── gui/ │ ├── main_gui.py # Glavni grafički interfejs │ ├── book_gui.py # GUI za knjige │ ├── author_gui.py # GUI za autore │ ├── category_gui.py # GUI za kategorije │ ├── publisher_gui.py # GUI za izdavače │ ├── member_gui.py # GUI za članove │ ├── reservation_gui.py # GUI za rezervacije │ └── transaction_gui.py # GUI za transakcije ├── services/ │ ├── book_service.py # Servisi za knjige │ ├── author_service.py # Servisi za autore │ ├── category_service.py # Servisi za kategorije │ ├── publisher_service.py # Servisi za izdavače │ ├── member_service.py # Servisi za članove │ ├── reservation_service.py # Servisi za rezervacije │ └── transaction_service.py # Servisi za transakcije ├── app.py # Ulazna tačka aplikacije └── requirements.txt # Lista potrebnih biblioteka

