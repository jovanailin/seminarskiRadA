import tkinter as tk
from tkinter import messagebox
from services.publisher_service import (
    add_new_publisher,
    find_publisher_by_id,
    search_publishers_by_name,
    list_all_publishers_with_count,
    update_publisher,
    remove_publisher,
    get_publishers_with_associated_books,
)

from sqlalchemy.orm import Session

class PublisherGUI:
    def __init__(self, root, session: Session):
        self.session = session
        self.root = root
        self.root.title("Manage Publishers")
        self.root.geometry("700x500")

        # Title
        title_label = tk.Label(root, text="Publisher Management", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        # Listbox for displaying publishers
        self.publishers_listbox = tk.Listbox(root, width=100, height=15)
        self.publishers_listbox.pack(pady=10)

        # Buttons for functionalities
        tk.Button(root, text="List All Publishers", command=self.load_publishers, width=25).pack(pady=5)
        tk.Button(root, text="Add New Publisher", command=self.open_add_publisher_window, width=25).pack(pady=5)
        tk.Button(root, text="Search Publishers by Name", command=self.open_search_publisher_window, width=25).pack(pady=5)
        tk.Button(root, text="Update Publisher Info", command=self.open_update_publisher_window, width=25).pack(pady=5)
        tk.Button(root, text="Remove Publisher", command=self.open_remove_publisher_window, width=25).pack(pady=5)

        # Load all publishers at startup
        self.load_publishers()

    def load_publishers(self):
    
        self.publishers_listbox.delete(0, tk.END)
        try:
            data = list_all_publishers_with_count(self.session)
            publishers = data.get("izdavači", [])  # Ispravljeno
            total_count = data.get("ukupan_broj", 0)  # Ispravljeno
            if not publishers:
                messagebox.showinfo("Info", "No publishers found in the database.")
                return
            for publisher in publishers:
                self.publishers_listbox.insert(
                    tk.END, f"{publisher.PublisherID}: {publisher.Name} - Contact: {publisher.ContactInfo}"
                )
            messagebox.showinfo("Total Publishers", f"Total publishers: {total_count}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def open_add_publisher_window(self):
        """Open a window to add a new publisher."""
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Publisher")
        add_window.geometry("400x300")

        # Input fields
        tk.Label(add_window, text="Name:").pack()
        name_entry = tk.Entry(add_window)
        name_entry.pack()

        tk.Label(add_window, text="Address:").pack()
        address_entry = tk.Entry(add_window)
        address_entry.pack()

        tk.Label(add_window, text="Contact Info:").pack()
        contact_info_entry = tk.Entry(add_window)
        contact_info_entry.pack()

        # Button to add publisher
        tk.Button(
            add_window,
            text="Add Publisher",
            command=lambda: self.add_publisher(
                name_entry.get(),
                address_entry.get(),
                contact_info_entry.get(),
            ),
        ).pack(pady=10)

    def add_publisher(self, name, address, contact_info):
        """Add a new publisher to the database."""
        try:
            if not name:
                raise ValueError("Publisher name is required.")
            add_new_publisher(self.session, name, address, contact_info)
            messagebox.showinfo("Success", f"Publisher '{name}' added successfully.")
            self.load_publishers()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def open_search_publisher_window(self):
        """Open a window to search publishers by name."""
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Publishers by Name")
        search_window.geometry("400x200")

        tk.Label(search_window, text="Enter Name:").pack()
        name_entry = tk.Entry(search_window)
        name_entry.pack()

        tk.Button(
            search_window, text="Search", command=lambda: self.search_publishers(name_entry.get())
        ).pack(pady=10)

    def search_publishers(self, name):
        """Search for publishers by name."""
        self.publishers_listbox.delete(0, tk.END)
        try:
            if not name:
                raise ValueError("Name cannot be empty.")
            publishers = search_publishers_by_name(self.session, name)
            for publisher in publishers:
                self.publishers_listbox.insert(
                    tk.END, f"{publisher.PublisherID}: {publisher.Name} - Contact: {publisher.ContactInfo}"
                )
            if not publishers:
                messagebox.showinfo("Search Result", "No publishers found with the given name.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def open_update_publisher_window(self):
        """Open a window to update publisher information."""
        update_window = tk.Toplevel(self.root)
        update_window.title("Update Publisher Info")
        update_window.geometry("400x300")

        tk.Label(update_window, text="Enter Publisher ID:").pack()
        publisher_id_entry = tk.Entry(update_window)
        publisher_id_entry.pack()

        tk.Label(update_window, text="New Name (optional):").pack()
        name_entry = tk.Entry(update_window)
        name_entry.pack()

        tk.Label(update_window, text="New Address (optional):").pack()
        address_entry = tk.Entry(update_window)
        address_entry.pack()

        tk.Label(update_window, text="New Contact Info (optional):").pack()
        contact_info_entry = tk.Entry(update_window)
        contact_info_entry.pack()

        tk.Button(
            update_window,
            text="Update Publisher",
            command=lambda: self.update_publisher(
                publisher_id_entry.get(),
                name_entry.get(),
                address_entry.get(),
                contact_info_entry.get(),
            ),
        ).pack(pady=10)

    def update_publisher(self, publisher_id, name, address, contact_info):
        """Update publisher information."""
        try:
            if not publisher_id:
                raise ValueError("Publisher ID is required.")
            kwargs = {k: v for k, v in [("Name", name), ("Address", address), ("ContactInfo", contact_info)] if v}
            update_publisher(self.session, int(publisher_id), **kwargs)
            messagebox.showinfo("Success", f"Publisher ID {publisher_id} updated successfully.")
            self.load_publishers()
        except ValueError:
            messagebox.showerror("Error", "Invalid ID. Please enter a number.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def open_remove_publisher_window(self):
        """Open a window to remove a publisher."""
        remove_window = tk.Toplevel(self.root)
        remove_window.title("Remove Publisher")
        remove_window.geometry("400x200")

        tk.Label(remove_window, text="Enter Publisher ID:").pack()
        publisher_id_entry = tk.Entry(remove_window)
        publisher_id_entry.pack()

        tk.Button(
            remove_window, text="Remove", command=lambda: self.remove_publisher(publisher_id_entry.get())
        ).pack(pady=10)

    def remove_publisher(self, publisher_id):
        """Delete a publisher from the database."""
        try:
            if not publisher_id:
                raise ValueError("Publisher ID is required.")
            remove_publisher(self.session, int(publisher_id))
            messagebox.showinfo("Success", f"Publisher ID {publisher_id} has been removed.")
            self.load_publishers()
        except ValueError:
            messagebox.showerror("Error", "Invalid ID. Please enter a number.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
