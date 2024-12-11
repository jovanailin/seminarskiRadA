from sqlalchemy.orm import Session # Za interakciju sa bazom podataka
from database.models import Book, Author, Publisher, Category, Member, Transaction, Reservation

# CRUD operacije

# Book operacije
def add_book(session: Session, title, author_id, publisher_id, isbn, category_id, shelf_location, total_copies, published_year):
    new_book = Book(
        Title=title,
        AuthorID=author_id,
        PublisherID=publisher_id,
        ISBN=isbn,
        CategoryID=category_id,
        ShelfLocation=shelf_location,
        TotalCopies=total_copies,
        AvailableCopies=total_copies,
        PublishedYear=published_year
    )
    session.add(new_book) 
    session.commit() 
    return new_book

def get_book_by_id(session: Session, book_id):
    return session.query(Book).filter_by(BookID=book_id).first()

def search_books_by_title(session, title):
    return session.query(Book).filter(Book.Title.ilike(f"%{title}%")).all()

def list_all_books(session):
    return session.query(Book).order_by(Book.BookID.asc()).all()

def update_book_availability(session: Session, book_id, available_copies):
    book = get_book_by_id(session, book_id)
    if book:
        book.AvailableCopies = available_copies
        session.commit()
    return book

def update_book_info(session, book_id, **kwargs):
    book = get_book_by_id(session, book_id)
    if not book:
        return None
    for key, value in kwargs.items():
        if hasattr(book, key):
            setattr(book, key, value)
    session.commit()
    return book

def delete_book(session: Session, book_id):
    book = get_book_by_id(session, book_id)
    if book:
        session.delete(book)
        session.commit()
    return book

def is_book_exists(session: Session, title: str, isbn: str):
    return session.query(Book).filter((Book.Title == title) | (Book.ISBN == isbn)).first() is not None

def is_book_available(session, book_id):
    book = get_book_by_id(session, book_id)
    return book and book.AvailableCopies > 0

def get_book_count(session):
    return session.query(Book).count()

def get_book_count_by_author(session: Session, author_id: int):
    return session.query(Book).filter_by(AuthorID=author_id).count()

# Author operacije
def add_author(session: Session, name, bio, nationality):
    new_author = Author(Name=name, Bio=bio, Nationality=nationality)
    session.add(new_author)
    session.commit()
    return new_author

def get_author_by_id(session: Session, author_id):
    return session.query(Author).filter_by(AuthorID=author_id).first()

def get_author_by_name(session: Session, name: str):
    return session.query(Author).filter(Author.Name.ilike(f"%{name}%")).all()

def list_all_authors(session: Session):
    return session.query(Author).all()

def is_author_exists(session: Session, name: str):
    return session.query(Author).filter(Author.Name.ilike(f"%{name}%")).first() is not None

def get_author_count(session: Session):
    return session.query(Author).count()

def get_authors_with_books(session: Session):
    return session.query(Author).outerjoin(Author.books).all()

def update_author_info(session: Session, author_id, **kwargs):
    author = get_author_by_id(session, author_id)
    if not author:
        return None
    for key, value in kwargs.items():
        if hasattr(author, key):
            setattr(author, key, value)
    session.commit()
    return author

def delete_author(session: Session, author_id: int):
    author = get_author_by_id(session, author_id)
    if author:
        session.delete(author)
        session.commit()
    return author

# Member operacije
def add_member(session: Session, name, address, contact_info, membership_date, membership_type):
    new_member = Member(
        Name=name,
        Address=address,
        ContactInfo=contact_info,
        MembershipDate=membership_date,
        MembershipType=membership_type
    )
    session.add(new_member)
    session.commit()
    return new_member

def get_member_by_id(session: Session, member_id):
    return session.query(Member).filter_by(MemberID=member_id).first()

def get_member_by_name(session: Session, name: str):
    return session.query(Member).filter(Member.Name.ilike(f"%{name}%")).all()

def list_all_members(session: Session):
    return session.query(Member).all()

def update_member_info(session: Session, member_id: int, **kwargs):
    member = get_member_by_id(session, member_id)
    if member:
        for key, value in kwargs.items():
            if hasattr(member, key):
                setattr(member, key, value)
        session.commit()
    return member

def delete_member(session: Session, member_id: int):
    member = get_member_by_id(session, member_id)
    if member:
        session.delete(member)
        session.commit()
    return member

def get_member_count(session: Session):
    return session.query(Member).count()

# Transaction operacije
def add_transaction(session: Session, book_id, member_id, borrow_date, due_date, status):
    new_transaction = Transaction(
        BookID=book_id,
        MemberID=member_id,
        BorrowDate=borrow_date,
        DueDate=due_date,
        Status=status
    )
    session.add(new_transaction)
    session.commit()
    return new_transaction

def update_transaction_return_date(session: Session, transaction_id, return_date):
    transaction = session.query(Transaction).filter_by(TransactionID=transaction_id).first()
    if transaction:
        transaction.ReturnDate = return_date
        session.commit()
    return transaction

def get_transaction_by_id(session: Session, transaction_id: int):
    return session.query(Transaction).filter_by(TransactionID=transaction_id).first()

def list_all_transactions(session: Session):
    return session.query(Transaction).all()

def get_transactions_by_book_id(session: Session, book_id: int):
    return session.query(Transaction).filter_by(BookID=book_id).all()

def get_transactions_by_member_id(session: Session, member_id: int):
    return session.query(Transaction).filter_by(MemberID=member_id).all()

def get_active_transactions(session: Session):
    return session.query(Transaction).filter(Transaction.Status != "Returned").all()

def get_transaction_count(session: Session):
    return session.query(Transaction).count()

def delete_transaction(session: Session, transaction_id: int):
    transaction = get_transaction_by_id(session, transaction_id)
    if transaction:
        session.delete(transaction)
        session.commit()
    return transaction

def get_transaction_count_by_member(session: Session, member_id: int):
    return session.query(Transaction).filter_by(MemberID=member_id).count()

def get_transaction_count_by_book(session: Session, book_id: int):
    return session.query(Transaction).filter_by(BookID=book_id).count()

# Reservation operacije
def add_reservation(session: Session, book_id, member_id, reservation_date, status):
    new_reservation = Reservation(
        BookID=book_id,
        MemberID=member_id,
        ReservationDate=reservation_date,
        Status=status
    )
    session.add(new_reservation)
    session.commit()
    return new_reservation

def get_reservation_by_id(session: Session, reservation_id):
    return session.query(Reservation).filter_by(ReservationID=reservation_id).first()

def list_all_reservations(session: Session):
    return session.query(Reservation).all()

def get_reservations_by_book_id(session: Session, book_id: int):
    return session.query(Reservation).filter_by(BookID=book_id).all()

def get_reservation_count_by_book(session: Session, book_id: int):
    return session.query(Reservation).filter_by(BookID=book_id).count()

def get_reservations_by_member_id(session: Session, member_id: int):
    return session.query(Reservation).filter_by(MemberID=member_id).all()

def get_reservation_count_by_member(session: Session, member_id: int):
    return session.query(Reservation).filter_by(MemberID=member_id).count()

def update_reservation_status(session: Session, reservation_id: int, new_status: str):
    reservation = get_reservation_by_id(session, reservation_id)
    if reservation:
        reservation.Status = new_status
        session.commit()
    return reservation

def delete_reservation(session: Session, reservation_id: int):
    reservation = get_reservation_by_id(session, reservation_id)
    if reservation:
        session.delete(reservation)
        session.commit()
    return reservation

def is_book_reserved(session: Session, book_id: int):
    return session.query(Reservation).filter_by(BookID=book_id, Status="Pending").first() is not None

def get_reservation_count(session: Session):
    return session.query(Reservation).count()

def get_active_reservations(session: Session):
    return session.query(Reservation).filter(Reservation.Status == "Pending").all()

# Category operacije
def add_category(session, category_name, description):
    category = Category(CategoryName=category_name, Description=description)
    session.add(category)
    session.commit()
    return category

def get_category_by_id(session, category_id):
    return session.query(Category).filter_by(CategoryID=category_id).first()

def get_category_by_name(session, category_name):
    return session.query(Category).filter(Category.CategoryName.ilike(f"%{category_name}%")).all()

def list_all_categories(session):
    return session.query(Category).all()

def update_category_info(session, category_id, **kwargs):
    category = get_category_by_id(session, category_id)
    if category:
        for key, value in kwargs.items():
            if hasattr(category, key):
                setattr(category, key, value)
        session.commit()
    return category

def delete_category(session, category_id):
    category = get_category_by_id(session, category_id)
    if category:
        session.delete(category)
        session.commit()
    return category

def get_category_count(session):
    return session.query(Category).count()

# Publisher Operations
def add_publisher(session, name, address, contact_info):
    publisher = Publisher(Name=name, Address=address, ContactInfo=contact_info)
    session.add(publisher)
    session.commit()
    return publisher

def get_publisher_by_id(session: Session, publisher_id: int):
    return session.query(Publisher).filter_by(PublisherID=publisher_id).first()

def get_publisher_by_name(session: Session, name: str):
    return session.query(Publisher).filter(Publisher.Name.ilike(f"%{name}%")).all()

def list_all_publishers(session: Session):
    return session.query(Publisher).all()

def update_publisher_info(session: Session, publisher_id: int, **kwargs):
    publisher = get_publisher_by_id(session, publisher_id)
    if publisher:
        for key, value in kwargs.items():
            if hasattr(publisher, key):
                setattr(publisher, key, value)
        session.commit()
    return publisher

def delete_publisher(session: Session, publisher_id: int):
    publisher = get_publisher_by_id(session, publisher_id)
    if publisher:
        session.delete(publisher)
        session.commit()
    return publisher

def get_publisher_count(session: Session):
    return session.query(Publisher).count()

def get_publishers_with_books(session: Session):
    return session.query(Publisher).outerjoin(Publisher.books).all()




