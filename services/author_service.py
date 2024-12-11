from database.db_operations import (
    add_author,
    get_author_by_id,
    update_author_info,
    delete_author,
    list_all_authors,
    get_author_by_name,
    is_author_exists as check_author_exists,
    get_book_count_by_author as book_count_by_author,
    get_authors_with_books as authors_with_books
)

# Author Service Functions
def add_new_author(name, bio, nationality, db_operations):
    if not name:
        raise ValueError("Ime je obavezno da bi se dodao autor.")
    if len(name) < 2:
        raise ValueError("Ima mora da ima najmanje 2 karaktera.")
    if check_author_exists(db_operations, name):
        raise ValueError(f"Autor '{name}'već postoji.")
    return add_author(db_operations, name, bio, nationality)

def find_author_by_id(author_id, db_operations):
    author = get_author_by_id(db_operations, author_id)
    if not author:
        raise ValueError(f"Ne postoji autor sa ID-jem {author_id}")
    return author

def find_author_by_name(name, db_operations):
    authors = get_author_by_name(db_operations, name)
    if not authors:  # Check if the list is empty
        raise ValueError(f"Ne postoji autor sa imenom '{name}'.")
    return authors

def list_all_authors_service(db_operations):
    authors = list_all_authors(db_operations)
    if not authors:
        print("Ne postoji nijedan autor u bazi.")
    return authors

def update_author_with_validation(author_id, db_operations, **kwargs):
    if not author_id:
        raise ValueError("ID autora je obavezan za ažuriranje.")
    if not kwargs:
        raise ValueError("Nijedno polje nije izmenjeno.")
    return update_author_info(db_operations, author_id, **kwargs)

def remove_author(author_id, db_operations):
    author = find_author_by_id(author_id, db_operations)
    return delete_author(db_operations, author.AuthorID)

def get_book_count_by_author_service(author_id, db_operations):
    if not author_id:
        raise ValueError("ID autora je obavezan.")
    return book_count_by_author(db_operations, author_id)

def get_authors_with_books_service(db_operations):
    return authors_with_books(db_operations)
