from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base
from utils.helpers import seed_initial_data

# Inicijalno postavljanje baze i testiranje konekcije

# Uspostavljanje konekcije sa bazom
DATABASE_URL = "postgresql+psycopg2://postgres:posejdon@localhost:5432/library"
engine = create_engine(DATABASE_URL)

# Kreiranje svih tabela u bazi podataka na osnovu modela iz models.py
# SQLAlchemy automatski prolazi kroz sve modele koji su deklarisani kao klase koje nasleđuju Base
def initialize_database():
    Base.metadata.create_all(engine)
    print("Database tables created successfully.")

SessionLocal = sessionmaker(bind=engine)

# Glavna funkcija za setup
def setup_database():
    initialize_database()
    session = SessionLocal()  
    try:
        seed_initial_data(session)
    finally:
        session.close()

if __name__ == "__main__":
    setup_database()
