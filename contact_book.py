import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class ContactBook:
    def __init__(self, filename="contacts.json"):
        self.filename = filename
        self.contacts = self.load_contacts()
    
    def load_contacts(self):
        """Load contacts from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_contacts(self):
        """Save contacts to JSON file"""
        with open(self.filename, 'w') as f:
            json.dump(self.contacts, f, indent=2)
    
    def add_contact(self, name, phone, email, address):
        """Add a new contact"""
        # Clean up inputs
        name = name.strip()
        phone = phone.strip()
        email = email.strip()
        address = address.strip()
        
        if not name or not phone:
            return False, "Name and Phone are required!"
        
        if phone in self.contacts:
            return False, "Phone number already exists!"
        
        self.contacts[phone] = {
            'name': name,
            'phone': phone,
            'email': email,
            'address': address
        }
        self.save_contacts()
        return True, "Contact added successfully!"
    
    def delete_contact(self, phone):
        """Delete a contact"""
        if phone in self.contacts:
            del self.contacts[phone]
            self.save_contacts()
            return True, "Contact deleted successfully!"
        return False, "Contact not found!"
    
    def update_contact(self, phone, name, email, address):
        """Update a contact"""
        phone = phone.strip()
        name = name.strip()
        email = email.strip()
        address = address.strip()
        
        if phone in self.contacts:
            self.contacts[phone]['name'] = name
            self.contacts[phone]['email'] = email
            self.contacts[phone]['address'] = address
            self.save_contacts()
            return True, "Contact updated successfully!"
        return False, "Contact not found!"
    
    def search_contact(self, query):
        """Search contacts by name or phone"""
        results = []
        query = query.lower()
        for phone, contact in self.contacts.items():
            if query in contact['name'].lower() or query in phone:
                results.append(contact)
        return results
    
    def get_all_contacts(self):
        """Get all contacts"""
        return list(self.contacts.values())


class ContactBookGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.root.geometry("800x600")
        self.root.config(bg="#f0f0f0")
        
        self.contact_book = ContactBook()
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        self.create_widgets()
        self.refresh_contact_list()
    
    def create_widgets(self):
        """Create GUI widgets"""
        # Title
        title = tk.Label(self.root, text="📞 Contact Book", font=("Arial", 20, "bold"), bg="#f0f0f0", fg="#333")
        title.pack(pady=10)
        
        # Frame for buttons
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="➕ Add Contact", command=self.add_contact_window, 
                 bg="#4CAF50", fg="white", font=("Arial", 10), padx=10).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="🔍 Search", command=self.search_window, 
                 bg="#2196F3", fg="white", font=("Arial", 10), padx=10).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="🔄 Refresh", command=self.refresh_contact_list, 
                 bg="#FF9800", fg="white", font=("Arial", 10), padx=10).pack(side=tk.LEFT, padx=5)
        
        # Frame for contact list
        list_frame = tk.Frame(self.root, bg="white")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview for contacts
        columns = ("Name", "Phone", "Email", "Address")
        self.tree = ttk.Treeview(list_frame, columns=columns, height=15, show='headings')
        
        for col in columns:
            self.tree.column(col, width=150)
            self.tree.heading(col, text=col)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double-click to edit and right-click for delete
        self.tree.bind("<Double-1>", self.on_tree_double_click)
        self.tree.bind("<Button-3>", self.on_right_click)
        
        # Frame for action buttons
        action_frame = tk.Frame(self.root, bg="#f0f0f0")
        action_frame.pack(pady=10)
        
        tk.Button(action_frame, text="✏️ Edit Selected", command=self.edit_contact, 
                 bg="#2196F3", fg="white", font=("Arial", 10), padx=10).pack(side=tk.LEFT, padx=5)
        tk.Button(action_frame, text="🗑️ Delete Selected", command=self.delete_contact, 
                 bg="#f44336", fg="white", font=("Arial", 10), padx=10).pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_label = tk.Label(self.root, text="No contacts", bg="#e0e0e0", font=("Arial", 9))
        self.status_label.pack(fill=tk.X)
    
    def refresh_contact_list(self):
        """Refresh the contact list display"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add all contacts
        contacts = self.contact_book.get_all_contacts()
        for contact in sorted(contacts, key=lambda x: x['name']):
            self.tree.insert('', tk.END, values=(
                contact['name'],
                contact['phone'],
                contact['email'],
                contact['address']
            ))
        
        # Update status
        self.status_label.config(text=f"Total Contacts: {len(contacts)}")
    
    def add_contact_window(self):
        """Open window to add a new contact"""
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Contact")
        add_window.geometry("400x300")
        add_window.config(bg="#f0f0f0")
        
        # Labels and entry fields
        tk.Label(add_window, text="Name:", font=("Arial", 10), bg="#f0f0f0").pack(pady=5)
        name_entry = tk.Entry(add_window, width=40, font=("Arial", 10))
        name_entry.pack(pady=5)
        
        tk.Label(add_window, text="Phone:", font=("Arial", 10), bg="#f0f0f0").pack(pady=5)
        phone_entry = tk.Entry(add_window, width=40, font=("Arial", 10))
        phone_entry.pack(pady=5)
        
        tk.Label(add_window, text="Email:", font=("Arial", 10), bg="#f0f0f0").pack(pady=5)
        email_entry = tk.Entry(add_window, width=40, font=("Arial", 10))
        email_entry.pack(pady=5)
        
        tk.Label(add_window, text="Address:", font=("Arial", 10), bg="#f0f0f0").pack(pady=5)
        address_entry = tk.Entry(add_window, width=40, font=("Arial", 10))
        address_entry.pack(pady=5)
        
        def save():
            name = name_entry.get()
            phone = phone_entry.get()
            email = email_entry.get()
            address = address_entry.get()
            
            success, message = self.contact_book.add_contact(name, phone, email, address)
            messagebox.showinfo("Result", message)
            
            if success:
                add_window.destroy()
                self.refresh_contact_list()
        
        tk.Button(add_window, text="Save Contact", command=save, 
                 bg="#4CAF50", fg="white", font=("Arial", 10), padx=20).pack(pady=20)
    
    def edit_contact(self):
        """Edit selected contact"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a contact to edit!")
            return
        
        item = selected[0]
        values = self.tree.item(item)['values']
        phone = str(values[1]).strip()
        
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Contact")
        edit_window.geometry("400x300")
        edit_window.config(bg="#f0f0f0")
        
        tk.Label(edit_window, text="Name:", font=("Arial", 10), bg="#f0f0f0").pack(pady=5)
        name_entry = tk.Entry(edit_window, width=40, font=("Arial", 10))
        name_entry.insert(0, values[0])
        name_entry.pack(pady=5)
        
        phone_label = tk.Label(edit_window, text=f"Phone: {phone}", font=("Arial", 10), bg="#f0f0f0")
        phone_label.pack(pady=5)
        
        tk.Label(edit_window, text="Email:", font=("Arial", 10), bg="#f0f0f0").pack(pady=5)
        email_entry = tk.Entry(edit_window, width=40, font=("Arial", 10))
        email_entry.insert(0, values[2])
        email_entry.pack(pady=5)
        
        tk.Label(edit_window, text="Address:", font=("Arial", 10), bg="#f0f0f0").pack(pady=5)
        address_entry = tk.Entry(edit_window, width=40, font=("Arial", 10))
        address_entry.insert(0, values[3])
        address_entry.pack(pady=5)
        
        def update():
            name = name_entry.get()
            email = email_entry.get()
            address = address_entry.get()
            
            success, message = self.contact_book.update_contact(phone, name, email, address)
            messagebox.showinfo("Result", message)
            
            if success:
                edit_window.destroy()
                self.refresh_contact_list()
        
        tk.Button(edit_window, text="Update Contact", command=update, 
                 bg="#2196F3", fg="white", font=("Arial", 10), padx=20).pack(pady=20)
    
    def delete_contact(self):
        """Delete selected contact"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a contact to delete!")
            return
        
        item = selected[0]
        phone = str(self.tree.item(item)['values'][1]).strip()
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this contact?"):
            success, message = self.contact_book.delete_contact(phone)
            messagebox.showinfo("Result", message)
            if success:
                self.refresh_contact_list()
    
    def search_window(self):
        """Open search window"""
        search_win = tk.Toplevel(self.root)
        search_win.title("Search Contact")
        search_win.geometry("400x150")
        search_win.config(bg="#f0f0f0")
        
        tk.Label(search_win, text="Search by Name or Phone:", font=("Arial", 10), bg="#f0f0f0").pack(pady=10)
        search_entry = tk.Entry(search_win, width=40, font=("Arial", 10))
        search_entry.pack(pady=10)
        
        def search():
            query = search_entry.get()
            if not query:
                messagebox.showwarning("Warning", "Please enter a search term!")
                return
            
            results = self.contact_book.search_contact(query)
            
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Add search results
            for contact in sorted(results, key=lambda x: x['name']):
                self.tree.insert('', tk.END, values=(
                    contact['name'],
                    contact['phone'],
                    contact['email'],
                    contact['address']
                ))
            
            self.status_label.config(text=f"Search Results: {len(results)} contact(s) found")
            search_win.destroy()
        
        tk.Button(search_win, text="Search", command=search, 
                 bg="#2196F3", fg="white", font=("Arial", 10), padx=20).pack(pady=10)
    
    def on_tree_double_click(self, event):
        """Handle double-click on tree item"""
        self.edit_contact()
    
    def on_right_click(self, event):
        """Handle right-click on tree item"""
        # Identify which item was clicked on
        item = self.tree.identify('item', event.x, event.y)
        if item:
            # Select the item first
            self.tree.selection_set(item)
            # Create and show context menu
            menu = tk.Menu(self.root, tearoff=0)
            menu.add_command(label="Edit", command=self.edit_contact)
            menu.add_command(label="Delete", command=self.delete_contact)
            menu.post(event.x_root, event.y_root)


if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBookGUI(root)
    root.mainloop()
