from database.db_operations import (
    add_category,
    get_category_by_id,
    get_category_by_name,
    list_all_categories,
    update_category_info,
    delete_category,
    get_category_count,
)

def add_new_category(session, category_name, description):
    if not category_name:
        raise ValueError("Naziv kategorije je obavezan.")
    if get_category_by_name(session, category_name):
        raise ValueError(f"Kategorija sa nazivom '{category_name}' već postoji.")
    return add_category(session, category_name, description)

def find_category_by_id(session, category_id):
    category = get_category_by_id(session, category_id)
    if not category:
        raise ValueError(f"Nema kategorije sa ID-jem {category_id}.")
    return category

def search_category_by_name(session, category_name):
    categories = get_category_by_name(session, category_name)
    if not categories:
        raise ValueError(f"Nema kategorija koje odgovaraju nazivu '{category_name}'.")
    return categories

def list_all_categories_with_count(session):
    categories = list_all_categories(session)
    count = get_category_count(session)
    return {"kategorije": categories, "ukupan_broj": count}

def update_category(session, category_id, **kwargs):
    if not kwargs:
        raise ValueError("Nisu navedene izmene.")
    category = find_category_by_id(session, category_id)
    updated_category = update_category_info(session, category_id, **kwargs)
    return updated_category

def remove_category(session, category_id):
    category = find_category_by_id(session, category_id)
    delete_category(session, category_id)
    return f"Kategorija sa ID-jem {category_id} je obrisana."
