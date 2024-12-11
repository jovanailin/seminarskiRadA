from database.db_operations import (
    add_publisher,
    get_publisher_by_id,
    get_publisher_by_name,
    list_all_publishers,
    update_publisher_info,
    delete_publisher,
    get_publisher_count,
    get_publishers_with_books,
)

def add_new_publisher(session, name, address, contact_info):
    if not name:
        raise ValueError("Naziv izdavača je obavezan.")
    if get_publisher_by_name(session, name):
        raise ValueError(f"Izdavač sa nazivom '{name}' već postoji.")
    return add_publisher(session, name, address, contact_info)

def find_publisher_by_id(session, publisher_id):
    publisher = get_publisher_by_id(session, publisher_id)
    if not publisher:
        raise ValueError(f"Nema izdavača sa ID-jem {publisher_id}.")
    return publisher

def search_publishers_by_name(session, name):
    publishers = get_publisher_by_name(session, name)
    if not publishers:
        raise ValueError(f"Nema izdavača koji odgovaraju nazivu '{name}'.")
    return publishers

def list_all_publishers_with_count(session):
    publishers = list_all_publishers(session)
    count = get_publisher_count(session)
    return {"izdavači": publishers, "ukupan_broj": count}

def update_publisher(session, publisher_id, **kwargs):
    if not kwargs:
        raise ValueError("Nisu navedene izmene.")
    publisher = find_publisher_by_id(session, publisher_id)
    updated_publisher = update_publisher_info(session, publisher_id, **kwargs)
    return updated_publisher

def remove_publisher(session, publisher_id):
    publisher = find_publisher_by_id(session, publisher_id)
    delete_publisher(session, publisher_id)
    return f"Izdavač sa ID-jem {publisher_id} je obrisan."

def get_publishers_with_associated_books(session):
    publishers = get_publishers_with_books(session)
    return publishers