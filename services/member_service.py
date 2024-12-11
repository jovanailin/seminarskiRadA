from sqlalchemy.orm import Session
from database.db_operations import (
    add_member,
    get_member_by_id,
    get_member_by_name,
    list_all_members,
    update_member_info,
    delete_member,
    get_member_count
)

def add_new_member(session: Session, name, address, contact_info, membership_date, membership_type):
    if not name or not membership_date or not membership_type:
        raise ValueError("Ime, datum članstva i tip članstva su obavezni.")
    return add_member(session, name, address, contact_info, membership_date, membership_type)

def find_member_by_id(session: Session, member_id):
    if not isinstance(member_id, int) or member_id <= 0:
        raise ValueError("Nevažeći ID člana.")
    member = get_member_by_id(session, member_id)
    if not member:
        print(f"Nema člana sa ID-jem {member_id}.")
    return member

def find_members_by_name(session: Session, name: str):
    if not name:
        raise ValueError("Ime ne može biti prazno.")
    return get_member_by_name(session, name)

def list_all_members_service(session: Session):
    members = list_all_members(session)
    if not members:
        print("Nema članova u biblioteci.")
    return members

def update_member_info_with_validation(session: Session, member_id, **kwargs):
    if not isinstance(member_id, int) or member_id <= 0:
        raise ValueError("Nevažeći ID člana.")
    if not kwargs:
        raise ValueError("Nisu navedene izmene.")
    member = update_member_info(session, member_id, **kwargs)
    if member:
        print(f"Član sa ID-jem {member_id} je uspešno ažuriran.")
    else:
        print(f"Nema člana sa ID-jem {member_id}.")
    return member

def remove_member(session: Session, member_id):
    if not isinstance(member_id, int) or member_id <= 0:
        raise ValueError("Nevažeći ID člana.")
    member = delete_member(session, member_id)
    if member:
        print(f"Član sa ID-jem {member_id} je obrisan.")
    else:
        print(f"Nema člana sa ID-jem {member_id}.")
    return member

def get_total_member_count(session: Session):
    count = get_member_count(session)
    print(f"Ukupan broj članova: {count}")
    return count
