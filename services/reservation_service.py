from sqlalchemy.orm import Session
from database.db_operations import (
    add_reservation,
    get_reservation_by_id,
    list_all_reservations,
    get_reservations_by_book_id,
    get_reservation_count_by_book,
    get_reservations_by_member_id,
    get_reservation_count_by_member,
    update_reservation_status,
    delete_reservation,
    is_book_reserved,
    get_reservation_count,
    get_active_reservations,
)
from database.models import Reservation
from datetime import date

def create_reservation(session: Session, book_id, member_id, reservation_date, status="Pending"):
    if is_book_reserved(session, book_id):
        print(f"Knjiga sa ID-jem {book_id} je već rezervisana.")
        return None

    new_reservation = add_reservation(session, book_id, member_id, reservation_date, status)
    print(f"Rezervacija kreirana za knjigu sa ID-jem {book_id} od strane člana sa ID-jem {member_id}.")
    return new_reservation

def find_reservation_by_id(session: Session, reservation_id):
    reservation = get_reservation_by_id(session, reservation_id)
    if reservation:
        return reservation
    else:
        print(f"Nema rezervacije sa ID-jem {reservation_id}.")
        return None

def list_all_active_reservations(session: Session):
    active_reservations = get_active_reservations(session)
    print(f"Pronađeno {len(active_reservations)} aktivnih rezervacija.")
    return active_reservations

def list_reservations_by_member(session: Session, member_id):
    reservations = get_reservations_by_member_id(session, member_id)
    print(f"Pronađeno {len(reservations)} rezervacija za člana sa ID-jem {member_id}.")
    return reservations

def list_reservations_by_book(session: Session, book_id):
    reservations = get_reservations_by_book_id(session, book_id)
    print(f"Pronađeno {len(reservations)} rezervacija za knjigu sa ID-jem {book_id}.")
    return reservations

def update_reservation_status_service(session: Session, reservation_id, new_status):
    reservation = find_reservation_by_id(session, reservation_id)
    if not reservation:
        print(f"Nema rezervacije sa ID-jem {reservation_id}.")
        return None

    updated_reservation = update_reservation_status(session, reservation_id, new_status)
    print(f"Rezervacija sa ID-jem {reservation_id} ažurirana na status '{new_status}'.")
    return updated_reservation

def cancel_reservation(session: Session, reservation_id):
    reservation = find_reservation_by_id(session, reservation_id)
    if reservation:
        delete_reservation(session, reservation_id)
        print(f"Rezervacija sa ID-jem {reservation_id} je otkazana.")
    else:
        print(f"Nema rezervacije sa ID-jem {reservation_id}.")

def count_reservations_by_member(session: Session, member_id):
    count = get_reservation_count_by_member(session, member_id)
    print(f"Član sa ID-jem {member_id} ima {count} rezervacija.")
    return count

def count_reservations_by_book(session: Session, book_id):
    count = get_reservation_count_by_book(session, book_id)
    print(f"Knjiga sa ID-jem {book_id} ima {count} rezervacija.")
    return count

def list_all_reservations_service(session: Session):
    all_reservations = list_all_reservations(session)
    print(f"Pronađeno {len(all_reservations)} ukupnih rezervacija.")
    return all_reservations

def validate_reservation_date(reservation_date):
    if reservation_date < date.today():
        raise ValueError("Datum rezervacije ne može biti u prošlosti.")
    print("Datum rezervacije je validan.")
