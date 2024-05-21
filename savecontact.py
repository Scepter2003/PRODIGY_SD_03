import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class ContactManager:
    def __init__(self):
        self.contacts = []

    def add_contact(self, name, phone, email):
        self.contacts.append(Contact(name, phone, email))

    def view_contact(self, index):
        return self.contacts[index]

    def save_contacts(self, filename):
        with open(filename, 'w') as f:
            for contact in self.contacts:
                f.write(f"{contact.name},{contact.phone},{contact.email}\n")

    def load_contacts(self, filename):
        self.contacts = []
        with open(filename, 'r') as f:
            for line in f:
                name, phone, email = line.strip().split(',')
                self.add_contact(name, phone, email)

    def delete_contact(self, index):
        del self.contacts[index]

class Contact:
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email

class ContactManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager")

        self.manager = ContactManager()

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.tab1 = ttk.Frame(self.notebook, width=400, height=400)
        self.tab2 = ttk.Frame(self.notebook, width=400, height=400)
        self.tab3 = ttk.Frame(self.notebook, width=400, height=400)

        self.notebook.add(self.tab1, text="Storage File")
        self.notebook.add(self.tab2, text="View Contacts")
        self.notebook.add(self.tab3, text="Add/Delete Contacts")

        self.create_tab1()
        self.create_tab2()
        self.create_tab3()

        self.filename = ""

    def create_tab1(self):
        self.filename_label = ttk.Label(self.tab1, text="Filename:")
        self.filename_label.grid(row=0, column=0, padx=10, pady=10)

        self.filename_entry = ttk.Entry(self.tab1)
        self.filename_entry.grid(row=0, column=1, padx=10, pady=10)

        self.load_button = ttk.Button(self.tab1, text="Load Contacts", command=self.load_contacts)
        self.load_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.create_button = ttk.Button(self.tab1, text="Create File", command=self.create_file)
        self.create_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def create_tab2(self):
        self.contact_listbox = tk.Listbox(self.tab2, width=50, height=10)
        self.contact_listbox.pack(padx=10, pady=10)

        self.view_button = ttk.Button(self.tab2, text="View Contact", command=self.view_contact)
        self.view_button.pack(padx=10, pady=10)

        self.view_container = ttk.LabelFrame(self.tab2, text="Contact Details")
        self.view_container.pack(padx=10, pady=10)

        self.name_label = ttk.Label(self.view_container, text="Name:")
        self.name_label.grid(row=0, column=0, padx=10, pady=10)

        self.name_value = ttk.Label(self.view_container, text="")
        self.name_value.grid(row=0, column=1, padx=10, pady=10)

        self.phone_label = ttk.Label(self.view_container, text="Phone:")
        self.phone_label.grid(row=1, column=0, padx=10, pady=10)

        self.phone_value = ttk.Label(self.view_container, text="")
        self.phone_value.grid(row=1, column=1, padx=10, pady=10)

        self.email_label = ttk.Label(self.view_container, text="Email:")
        self.email_label.grid(row=2, column=0, padx=10, pady=10)

        self.email_value = ttk.Label(self.view_container, text="")
        self.email_value.grid(row=2, column=1, padx=10, pady=10)

        self.delete_button = ttk.Button(self.view_container, text="Delete Contact", state=tk.DISABLED, command=self.delete_contact)
        self.delete_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def create_tab3(self):
        self.name_label = ttk.Label(self.tab3, text="Name:")
        self.name_label.grid(row=0,column=0, padx=10, pady=10)

        self.name_entry = ttk.Entry(self.tab3)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.phone_label = ttk.Label(self.tab3, text="Phone:")
        self.phone_label.grid(row=1, column=0, padx=10, pady=10)

        self.phone_entry = ttk.Entry(self.tab3)
        self.phone_entry.grid(row=1, column=1, padx=10, pady=10)

        self.email_label = ttk.Label(self.tab3, text="Email:")
        self.email_label.grid(row=2, column=0, padx=10, pady=10)

        self.email_entry = ttk.Entry(self.tab3)
        self.email_entry.grid(row=2, column=1, padx=10, pady=10)

        self.add_button = ttk.Button(self.tab3, text="Add Contact", command=self.add_contact)
        self.add_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def load_contacts(self):
        filename = filedialog.askopenfilename(filetypes=[("", "")])
        if filename:
            self.filename = filename
            self.manager.load_contacts(filename)
            self.update_contact_listbox()
            self.filename_entry.delete(0, tk.END)
            self.filename_entry.insert(0, filename)

    def create_file(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv")
        if filename:
            self.filename = filename
            self.manager.save_contacts(filename)
            self.filename_entry.delete(0, tk.END)
            self.filename_entry.insert(0, filename)

    def update_contact_listbox(self):
        self.contact_listbox.delete(0, tk.END)
        for i, contact in enumerate(self.manager.contacts):
            self.contact_listbox.insert(tk.END, f"{i + 1}. {contact.name}")

    def add_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()

        self.manager.add_contact(name, phone, email)

        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

        self.update_contact_listbox()
        self.load_contacts(self.filename)

    def view_contact(self):
        selected_index = self.contact_listbox.curselection()
        if selected_index:
            contact_index = int(selected_index[0])
            selected_contact = self.manager.view_contact(contact_index)

            self.name_value.config(text=selected_contact.name)
            self.phone_value.config(text=selected_contact.phone)
            self.email_value.config(text=selected_contact.email)

            self.delete_button.config(state=tk.NORMAL)
        else:
            self.name_value.config(text="")
            self.phone_value.config(text="")
            self.email_value.config(text="")

            self.delete_button.config(state=tk.DISABLED)

    def delete_contact(self):
        selected_index = self.contact_listbox.curselection()
        if selected_index:
            contact_index = int(selected_index[0])
            self.manager.delete_contact(contact_index)
            self.update_contact_listbox()
            self.load_contacts(self.filename)

            self.name_value.config(text="")
            self.phone_value.config(text="")
            self.email_value.config(text="")

            self.delete_button.config(state=tk.DISABLED)
root = tk.Tk()

app = ContactManagerGUI(root)
root.mainloop()
