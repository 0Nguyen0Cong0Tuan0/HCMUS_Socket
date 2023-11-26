import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

class EmailViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Viewer")
        self.root.geometry("600x400")

        # Apply ttkbootstrap style
        self.style = Style(theme="darkly")

        # Create a treeview
        self.tree = ttk.Treeview(self.root, style="Treeview")
        self.tree["columns"] = ("Subject", "From", "Date")
        self.tree.heading("#0", text="Folder", anchor=tk.W)
        self.tree.heading("Subject", text="Subject", anchor=tk.W)
        self.tree.heading("From", text="From", anchor=tk.W)
        self.tree.heading("Date", text="Date", anchor=tk.W)
        self.tree.column("#0", width=150)
        self.tree.column("Subject", width=200)
        self.tree.column("From", width=150)
        self.tree.column("Date", width=100)
        self.tree.pack(expand=tk.YES, fill=tk.BOTH)

        # Insert sample data
        self.insert_folder("Inbox")
        self.insert_email("Inbox", "Email 1", "john.doe@example.com", "2023-01-01")
        self.insert_email("Inbox", "Email 2", "jane.smith@example.com", "2023-01-02")

        # Bind double-click event to show email content
        self.tree.bind("<Double-1>", self.show_email_content)

    def insert_folder(self, folder_name):
        self.tree.insert("", "end", folder_name, text=folder_name)

    def insert_email(self, folder_name, subject, sender, date):
        self.tree.insert(folder_name, "end", text="", values=(subject, sender, date))

    def show_email_content(self, event):
        item = self.tree.selection()[0]
        if not self.tree.parent(item):  # Check if it's not a child node (i.e., an email)
            return
        folder_name = self.tree.parent(item)
        email_subject = self.tree.item(item, "values")[0]

        # You can implement logic to fetch and display the content of the selected email
        print(f"Selected email: {email_subject} in folder {folder_name}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmailViewer(root)
    root.mainloop()
