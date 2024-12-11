from sqlalchemy import create_engine, Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

# Definisanje osnovne klase za ORM modele
Base = declarative_base()

# Definisanje tabela (klasa)

class Book(Base):
    __tablename__ = 'books'

    BookID = Column(Integer, primary_key=True)
    Title = Column(String, nullable=False)
    AuthorID = Column(Integer, ForeignKey('authors.AuthorID'), nullable=False)
    PublisherID = Column(Integer, ForeignKey('publishers.PublisherID'), nullable=False)
    ISBN = Column(String)
    CategoryID = Column(Integer, ForeignKey('categories.CategoryID'))
    ShelfLocation = Column(String)
    TotalCopies = Column(Integer)
    AvailableCopies = Column(Integer)
    PublishedYear = Column(Integer)

    # Postavljanje dvosmerne relacije između dve tabele
    # Ove relacije su samo na nivou python-a
    author = relationship('Author', back_populates='books')
    publisher = relationship('Publisher', back_populates='books')
    category = relationship('Category', back_populates='books')
    transactions = relationship('Transaction', back_populates='book')
    reservations = relationship('Reservation', back_populates='book')

class Author(Base):
    __tablename__ = 'authors'

    AuthorID = Column(Integer, primary_key=True)
    Name = Column(String, nullable=False)
    Bio = Column(Text)
    Nationality = Column(String)

    books = relationship('Book', back_populates='author')

class Publisher(Base):
    __tablename__ = 'publishers'

    PublisherID = Column(Integer, primary_key=True)
    Name = Column(String, nullable=False)
    Address = Column(Text)
    ContactInfo = Column(String)

    books = relationship('Book', back_populates='publisher')

class Category(Base):
    __tablename__ = 'categories'

    CategoryID = Column(Integer, primary_key=True)
    CategoryName = Column(String, nullable=False)
    Description = Column(Text)

    books = relationship('Book', back_populates='category')

class Member(Base):
    __tablename__ = 'members'

    MemberID = Column(Integer, primary_key=True)
    Name = Column(String, nullable=False)
    Address = Column(Text)
    ContactInfo = Column(String)
    MembershipDate = Column(Date)
    MembershipType = Column(String)

    transactions = relationship('Transaction', back_populates='member')
    reservations = relationship('Reservation', back_populates='member')

class Transaction(Base):
    __tablename__ = 'transactions'

    TransactionID = Column(Integer, primary_key=True)
    BookID = Column(Integer, ForeignKey('books.BookID'), nullable=False)
    MemberID = Column(Integer, ForeignKey('members.MemberID'), nullable=False)
    BorrowDate = Column(Date)
    DueDate = Column(Date)
    ReturnDate = Column(Date)
    Status = Column(String)

    book = relationship('Book', back_populates='transactions')
    member = relationship('Member', back_populates='transactions')

class Reservation(Base):
    __tablename__ = 'reservations'

    ReservationID = Column(Integer, primary_key=True)
    BookID = Column(Integer, ForeignKey('books.BookID'), nullable=False)
    MemberID = Column(Integer, ForeignKey('members.MemberID'), nullable=False)
    ReservationDate = Column(Date)
    Status = Column(String)

    book = relationship('Book', back_populates='reservations')
    member = relationship('Member', back_populates='reservations')
