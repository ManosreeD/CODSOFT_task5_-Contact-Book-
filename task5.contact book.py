import tkinter as tk
from tkinter import messagebox
import re

class ContactBook:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.root.geometry("500x600")
        self.root.configure(bg="light green")
        
        # Contact storage (for simplicity, using a dictionary)
        self.contacts = {}
        
        # GUI Elements
        self.name_label = tk.Label(root, text="Name")
        self.name_label.grid(row=0, column=0, padx=10, pady=10)
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        self.phone_label = tk.Label(root, text="Phone Number")
        self.phone_label.grid(row=1, column=0, padx=10, pady=10)
        self.phone_entry = tk.Entry(root)
        self.phone_entry.grid(row=1, column=1, padx=10, pady=10)

        self.mail_label = tk.Label(root, text="Email")
        self.mail_label.grid(row=2, column=0, padx=10, pady=10)
        self.mail_entry = tk.Entry(root)
        self.mail_entry.grid(row=2, column=1, padx=10, pady=10)

        self.address_label = tk.Label(root, text="Address")
        self.address_label.grid(row=3, column=0, padx=10, pady=10)
        self.address_entry = tk.Entry(root)
        self.address_entry.grid(row=3, column=1, padx=10, pady=10)
        
        self.add_btn = tk.Button(root, text="Add Contact", command=self.add_contact)
        self.add_btn.grid(row=4, column=0, padx=10, pady=10)
        
        self.view_btn = tk.Button(root, text="View Contacts", command=self.view_contacts)
        self.view_btn.grid(row=4, column=1, padx=10, pady=10)
        
        self.update_btn = tk.Button(root, text="Update Contact", command=self.update_contact)
        self.update_btn.grid(row=5, column=0, padx=10, pady=10)
        
        self.delete_btn = tk.Button(root, text="Delete Contact", command=self.delete_contact)
        self.delete_btn.grid(row=5, column=1, padx=10, pady=10)
        
        self.search_btn = tk.Button(root, text="Search Contact", command=self.search_contact)
        self.search_btn.grid(row=6, column=0, padx=10, pady=10)

        self.search_entry = tk.Entry(root)
        self.search_entry.grid(row=6, column=1, padx=10, pady=10)

        # Frame for Listbox and Scrollbars
        self.listbox_frame = tk.Frame(root)
        self.listbox_frame.grid(row=15, column=0, columnspan=2, padx=10, pady=10)

        # Scrollbars
        self.v_scrollbar = tk.Scrollbar(self.listbox_frame, orient=tk.VERTICAL)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.h_scrollbar = tk.Scrollbar(self.listbox_frame, orient=tk.HORIZONTAL)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Listbox
        self.listbox_contacts = tk.Listbox(self.listbox_frame, height=10, width=50, yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)
        self.listbox_contacts.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configure scrollbars
        self.v_scrollbar.config(command=self.listbox_contacts.yview)
        self.h_scrollbar.config(command=self.listbox_contacts.xview)

        self.exit_btn = tk.Button(root, text="Exit", command=self.root.quit)
        self.exit_btn.grid(row=16, column=0, padx=10, pady=10)

        self.clr_btn = tk.Button(root, text="Clear", command=self.clear_listbox)
        self.clr_btn.grid(row=16, column=1, padx=10, pady=10)
        
    def add_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.mail_entry.get()
        address = self.address_entry.get()
        
        if name and phone and self.is_valid_phone(phone) and self.is_valid_email(email):
            if name in self.contacts:
                messagebox.showerror("Error", "Contact with this name already exists. Please use a different name or update the existing contact.")
            else:
                self.contacts[name] = {
                    'phone': phone,
                    'email': email,
                    'address': address
                }
                messagebox.showinfo("Success", "Contact added successfully!")
                self.clear_entries()
        else:
            messagebox.showerror("Error", "Please enter valid details: Name, Phone number (valid format), and Email (valid format).")
    
    def view_contacts(self):
        self.listbox_contacts.delete(0, tk.END)
        if self.contacts:
            for name, info in self.contacts.items():
                self.listbox_contacts.insert(tk.END, f"Name: {name}, Phone: {info['phone']}, Email: {info['email']}, Address: {info['address']}")
        else:
            self.listbox_contacts.insert(tk.END, "No contacts available.")
    
    def update_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.mail_entry.get()
        address = self.address_entry.get()
        
        if name in self.contacts:
            if phone and self.is_valid_phone(phone) and email and self.is_valid_email(email):
                self.contacts[name] = {
                    'phone': phone,
                    'email': email,
                    'address': address
                }
                messagebox.showinfo("Success", "Contact updated successfully!")
                self.clear_entries()
                self.view_contacts()  # Refresh the listbox to reflect the update
            else:
                messagebox.showerror("Error", "Please enter valid details: Phone number (valid format) and Email (valid format).")
        else:
            messagebox.showerror("Error", "Contact not found.")
    
    def delete_contact(self):
        try:
            selected_index = self.listbox_contacts.curselection()[0]
            contact_to_delete = self.listbox_contacts.get(selected_index).split(",")[0].split(": ")[1]
            if contact_to_delete in self.contacts:
                del self.contacts[contact_to_delete]
                self.listbox_contacts.delete(selected_index)
                messagebox.showinfo("Success", "Contact deleted successfully!")
            else:
                messagebox.showerror("Warning", "Selected contact could not be found.")
        except IndexError:
            messagebox.showerror("Warning", "Select a contact to delete.")
        except KeyError:
            messagebox.showerror("Warning", "Selected contact could not be found.")
    
    def search_contact(self):
        search = self.search_entry.get()
        self.listbox_contacts.delete(0, tk.END)
        
        if search:
            found = False
            for name, info in self.contacts.items():
                if search.lower() in name.lower():
                    self.listbox_contacts.insert(tk.END, f"Name: {name}, Phone: {info['phone']}, Email: {info['email']}, Address: {info['address']}")
                    found = True
            if not found:
                self.listbox_contacts.insert(tk.END, "Contact not found.")
        else:
            self.listbox_contacts.insert(tk.END, "Please enter a name to search.")
        
        self.search_entry.delete(0, tk.END)
    
    def clear_listbox(self):
        self.listbox_contacts.delete(0, tk.END)
        
    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.mail_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)

    def is_valid_phone(self, phone):
        # Simple validation for phone number (e.g., (123) 456-7890)
        return re.match(r'^\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{4}$', phone) is not None

    def is_valid_email(self, email):
        # Simple validation for email
        return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) is not None

# Main program entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBook(root)
    root.mainloop()

     
