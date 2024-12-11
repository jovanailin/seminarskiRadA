import tkinter as tk
from gui.main_gui import MainGUI  # Ensure this path is correct
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.db_setup import DATABASE_URL

def run_app():
    root = tk.Tk()
    root.title("Library Management System")

    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    app = MainGUI(root, session)

    root.mainloop()

    session.close()

if __name__ == "__main__":
    run_app()
