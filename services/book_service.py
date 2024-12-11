from sqlalchemy.orm import Session
from database.db_operations import (
    add_book,
    get_book_by_id,
    update_book_availability,
    delete_book,
    get_book_count,
    is_book_available,
    update_book_info,
    search_books_by_title,
    list_all_books,
)
from database.models import Book

# Book Service Funkcije
def add_new_book(session: Session, title, author_id, publisher_id, isbn, category_id, shelf_location, total_copies, published_year):
    if not all([title, author_id, publisher_id, isbn]):
        raise ValueError("Naslov, Autor ID, Izdavač ID i ISBN su obavezni.")
    if total_copies < 0:
        raise ValueError("Ukupne kopije ne mogu biti negativne.")
    return add_book(session, title, author_id, publisher_id, isbn, category_id, shelf_location, total_copies, published_year)

def find_book_by_id(session: Session, book_id):
    book = get_book_by_id(session, book_id)
    if not book:
        raise ValueError(f"Nije pronađena knjiga sa ID-em {book_id}")
    return book

def search_books_by_title_service(session: Session, title):
    return search_books_by_title(session, title)

def list_all_books_service(session: Session):
    return list_all_books(session)

def check_book_availability(session: Session, book_id):
    if not book_id:
        raise ValueError("ID knjige je obavezan.")
    is_available = is_book_available(session, book_id)
    return is_available

def get_total_book_count(session: Session):
    return get_book_count(session)

def update_book_copies(session: Session, book_id, available_copies):
    if available_copies < 0:
        raise ValueError("Dostupne kopije ne mogu biti negativne.")
    book = find_book_by_id(session, book_id)
    updated_book = update_book_availability(session, book_id, available_copies)
    return updated_book

def update_book_info_with_validation(session: Session, book_id, **kwargs):
    book = find_book_by_id(session, book_id)
    if not kwargs:
        raise ValueError("Nisu navedene izmene.")
    return update_book_info(session, book_id, **kwargs)

def remove_book(session: Session, book_id):
    book = find_book_by_id(session, book_id)
    return delete_book(session, book_id)
