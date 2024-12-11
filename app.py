import tkinter as tk
from gui.main_gui import MainGUI  # Ensure this path is correct
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.db_setup import DATABASE_URL

def run_app():
    """Run the Library Management System application."""
    root = tk.Tk()
    root.title("Library Management System")

    # Create the SQLAlchemy engine and session
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Pass the session to MainGUI
    app = MainGUI(root, session)

    # Start the Tkinter event loop
    root.mainloop()

    # Close the session upon exiting
    session.close()

if __name__ == "__main__":
    run_app()
