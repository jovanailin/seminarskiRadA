from sqlalchemy.orm import Session
from database.db_operations import (
    add_transaction,
    update_transaction_return_date,
    get_transaction_by_id,
    list_all_transactions,
    get_transactions_by_book_id,
    get_transactions_by_member_id,
    get_active_transactions,
    delete_transaction,
    get_transaction_count,
    get_transaction_count_by_member,
    get_transaction_count_by_book,
    update_book_availability,
    get_book_by_id,
)
from datetime import date
from database.models import Transaction

def borrow_book(session: Session, book_id, member_id, borrow_date, due_date):
    book = get_book_by_id(session, book_id)
    if book and book.AvailableCopies > 0:
        new_transaction = add_transaction(session, book_id, member_id, borrow_date, due_date, "borrowed")
        update_book_availability(session, book_id, book.AvailableCopies - 1)
        print(f"Knjiga sa ID-jem {book_id} je pozajmljena članu sa ID-jem {member_id}.")
        return new_transaction
    else:
        print(f"Knjiga sa ID-jem {book_id} nije dostupna za pozajmicu.")
        return None

def return_book(session: Session, transaction_id, return_date):
    transaction = get_transaction_by_id(session, transaction_id)
    if transaction and transaction.Status == "borrowed":
        transaction = update_transaction_return_date(session, transaction_id, return_date)
        transaction.Status = "returned"
        session.commit()

        book = get_book_by_id(session, transaction.BookID)
        if book:
            update_book_availability(session, book.BookID, book.AvailableCopies + 1)
        print(f"Knjiga sa ID-jem {transaction.BookID} je vraćena od strane člana sa ID-jem {transaction.MemberID}.")
        return transaction
    else:
        print(f"Nema aktivne transakcije pozajmice sa ID-jem {transaction_id}.")
        return None

def list_all_transactions_service(session: Session):
    return list_all_transactions(session)

def list_member_transactions(session: Session, member_id):
    return get_transactions_by_member_id(session, member_id)

def list_active_borrowed_books(session: Session):
    return get_active_transactions(session)

def has_active_transactions(session: Session, member_id: int):
    active_transactions = session.query(Transaction).filter_by(MemberID=member_id, Status="borrowed").count()
    return active_transactions > 0

def list_overdue_transactions(session: Session):
    today = date.today()
    overdue_transactions = session.query(Transaction).filter(Transaction.DueDate < today, Transaction.Status == "borrowed").all()
    if not overdue_transactions:
        print("Nema prekoračenih transakcija.")
    return overdue_transactions

def get_active_borrow_count_by_book(session: Session, book_id: int):
    count = session.query(Transaction).filter_by(BookID=book_id, Status="borrowed").count()
    print(f"Knjiga sa ID-jem {book_id} je trenutno pozajmljena {count} puta.")
    return count

def list_transactions_by_status(session: Session, status: str):
    if status not in ["borrowed", "returned"]:
        raise ValueError("Nevažeći status transakcije.")
    transactions = session.query(Transaction).filter_by(Status=status).all()
    print(f"Pronađeno {len(transactions)} transakcija sa statusom '{status}'.")
    return transactions
