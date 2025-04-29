import customtkinter as ctk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
from base import Database

class LibraryManagementSystem:
    def __init__(self):
        self.db = Database("library.db")
        
        # Configure customtkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("Library Management System")
        self.root.geometry("1200x800")
        
        # Create main container
        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create tabs
        self.tabview = ctk.CTkTabview(self.main_container)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create tabs for different sections
        self.tab_books = self.tabview.add("Books")
        self.tab_members = self.tabview.add("Members")
        self.tab_borrowings = self.tabview.add("Borrowings")
        
        # Configure ttk style to match customtkinter theme
        # In the __init__ method, update the Treeview style configuration
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("Treeview", 
                            background="#2b2b2b", 
                            foreground="white", 
                            fieldbackground="#2b2b2b",
                            borderwidth=0,
                            font=('Arial', 12),
                            rowheight=30)
        self.style.configure("Treeview.Heading", 
                            background="#1f538d", 
                            foreground="white", 
                            relief="flat",
                            font=('Arial', 12, 'bold'),
                            padding=(10, 5))
        # Change the selection color to a different shade
        self.style.map("Treeview",
                      background=[("selected", "#3a7ebf")],  # Changed from #1f538d to #3a7ebf
                      foreground=[("selected", "#ffffff")])  # White text for selected items
        
        self.setup_books_tab()
        self.setup_members_tab()
        self.setup_borrowings_tab()
        
        self.root.mainloop()
    
    def setup_books_tab(self):
        # Book entry frame
        entry_frame = ctk.CTkFrame(self.tab_books)
        entry_frame.pack(fill="x", padx=10, pady=10)
        
        # Book entry fields
        self.book_title = ctk.CTkEntry(entry_frame, placeholder_text="Title")
        self.book_title.grid(row=0, column=0, padx=5, pady=5)
        
        self.book_author = ctk.CTkEntry(entry_frame, placeholder_text="Author")
        self.book_author.grid(row=0, column=1, padx=5, pady=5)
        
        self.book_isbn = ctk.CTkEntry(entry_frame, placeholder_text="ISBN")
        self.book_isbn.grid(row=0, column=2, padx=5, pady=5)
        
        self.book_category = ctk.CTkEntry(entry_frame, placeholder_text="Category")
        self.book_category.grid(row=1, column=0, padx=5, pady=5)
        
        self.book_quantity = ctk.CTkEntry(entry_frame, placeholder_text="Quantity")
        self.book_quantity.grid(row=1, column=1, padx=5, pady=5)
        
        # Books table
        self.books_tree = ttk.Treeview(self.tab_books, columns=("ID", "Title", "Author", "ISBN", "Category", "Quantity", "Available"), show="headings")
        for col in ("ID", "Title", "Author", "ISBN", "Category", "Quantity", "Available"):
            self.books_tree.heading(col, text=col)
            self.books_tree.column(col, anchor="center")
        
        # Set column widths
        self.books_tree.column("ID", width=50)
        self.books_tree.column("Title", width=200)
        self.books_tree.column("Author", width=150)
        self.books_tree.column("ISBN", width=100)
        self.books_tree.column("Category", width=100)
        self.books_tree.column("Quantity", width=80)
        self.books_tree.column("Available", width=80)
        
        self.books_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.books_tree.bind("<ButtonRelease-1>", self.select_book)
        self.load_books()
        
        # Add button frame after entry fields
        btn_frame = ctk.CTkFrame(entry_frame)
        btn_frame.grid(row=2, column=0, columnspan=3, pady=10)
        
        ctk.CTkButton(btn_frame, text="Add Book", command=self.add_book).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Update Book", command=self.update_book).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Delete Book", command=self.delete_book).pack(side="left", padx=5)
    
    def setup_members_tab(self):
        # Member entry frame
        entry_frame = ctk.CTkFrame(self.tab_members)
        entry_frame.pack(fill="x", padx=10, pady=10)
        
        # Member entry fields
        self.member_name = ctk.CTkEntry(entry_frame, placeholder_text="Name")
        self.member_name.grid(row=0, column=0, padx=5, pady=5)
        
        self.member_id = ctk.CTkEntry(entry_frame, placeholder_text="Member ID")
        self.member_id.grid(row=0, column=1, padx=5, pady=5)
        
        self.member_email = ctk.CTkEntry(entry_frame, placeholder_text="Email")
        self.member_email.grid(row=0, column=2, padx=5, pady=5)
        
        self.member_phone = ctk.CTkEntry(entry_frame, placeholder_text="Phone")
        self.member_phone.grid(row=1, column=0, padx=5, pady=5)
        
        # Members table
        self.members_tree = ttk.Treeview(self.tab_members, columns=("ID", "Name", "Member ID", "Email", "Phone", "Join Date"), show="headings")
        for col in ("ID", "Name", "Member ID", "Email", "Phone", "Join Date"):
            self.members_tree.heading(col, text=col)
            self.members_tree.column(col, anchor="center")
        
        # Set column widths
        self.members_tree.column("ID", width=50)
        self.members_tree.column("Name", width=150)
        self.members_tree.column("Member ID", width=100)
        self.members_tree.column("Email", width=200)
        self.members_tree.column("Phone", width=100)
        self.members_tree.column("Join Date", width=100)
        
        self.members_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.members_tree.bind("<ButtonRelease-1>", self.select_member)
        self.load_members()
        
        # Add button frame after entry fields
        btn_frame = ctk.CTkFrame(entry_frame)
        btn_frame.grid(row=2, column=0, columnspan=3, pady=10)
        
        ctk.CTkButton(btn_frame, text="Add Member", command=self.add_member).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Update Member", command=self.update_member).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Delete Member", command=self.delete_member).pack(side="left", padx=5)
    
    def setup_borrowings_tab(self):
        # Borrowing entry frame
        entry_frame = ctk.CTkFrame(self.tab_borrowings)
        entry_frame.pack(fill="x", padx=10, pady=10)
        
        # Borrowing entry fields
        self.borrow_book = ctk.CTkEntry(entry_frame, placeholder_text="Book ID")
        self.borrow_book.grid(row=0, column=0, padx=5, pady=5)
        
        self.borrow_member = ctk.CTkEntry(entry_frame, placeholder_text="Member ID")
        self.borrow_member.grid(row=0, column=1, padx=5, pady=5)
        
        # Buttons
        btn_frame = ctk.CTkFrame(entry_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        ctk.CTkButton(btn_frame, text="Borrow Book", command=self.borrow_book_action).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Return Book", command=self.return_book_action).pack(side="left", padx=5)
        
        # Borrowings table
        self.borrowings_tree = ttk.Treeview(self.tab_borrowings, 
            columns=("ID", "Book", "Member", "Borrow Date", "Borrow Time", "Return Date", "Status"), 
            show="headings")
        for col in ("ID", "Book", "Member", "Borrow Date", "Borrow Time", "Return Date", "Status"):
            self.borrowings_tree.heading(col, text=col)
            self.borrowings_tree.column(col, anchor="center")
        
        # Set column widths
        self.borrowings_tree.column("ID", width=50)
        self.borrowings_tree.column("Book", width=200)
        self.borrowings_tree.column("Member", width=150)
        self.borrowings_tree.column("Borrow Date", width=100)
        self.borrowings_tree.column("Borrow Time", width=100)  # New column
        self.borrowings_tree.column("Return Date", width=100)
        self.borrowings_tree.column("Status", width=100)
        
        self.borrowings_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.load_borrowings()
    
    # Book operations
    def add_book(self):
        try:
            title = self.book_title.get()
            author = self.book_author.get()
            isbn = self.book_isbn.get()
            category = self.book_category.get()
            quantity = int(self.book_quantity.get())
            
            if not all([title, author, isbn, category, quantity]):
                messagebox.showerror("Error", "Please fill all fields")
                return
            
            self.db.insert_book(title, author, isbn, category, quantity)
            messagebox.showinfo("Success", "Book added successfully")
            self.clear_book_fields()
            self.load_books()
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity")
    
    def update_book(self):
        selected_item = self.books_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a book to update")
            return
        
        try:
            book_id = self.books_tree.item(selected_item)['values'][0]
            title = self.book_title.get()
            author = self.book_author.get()
            isbn = self.book_isbn.get()
            category = self.book_category.get()
            quantity = int(self.book_quantity.get())
            
            if not all([title, author, isbn, category, quantity]):
                messagebox.showerror("Error", "Please fill all fields")
                return
            
            self.db.update_book(book_id, title, author, isbn, category, quantity)
            messagebox.showinfo("Success", "Book updated successfully")
            self.clear_book_fields()
            self.load_books()
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity")
    
    def clear_book_fields(self):
        self.book_title.delete(0, 'end')
        self.book_author.delete(0, 'end')
        self.book_isbn.delete(0, 'end')
        self.book_category.delete(0, 'end')
        self.book_quantity.delete(0, 'end')
    
    def add_member(self):
        try:
            name = self.member_name.get()
            member_id = self.member_id.get()
            email = self.member_email.get()
            phone = self.member_phone.get()
            join_date = datetime.now().strftime("%Y-%m-%d")
            
            if not all([name, member_id, email, phone]):
                messagebox.showerror("Error", "Please fill all fields")
                return
            
            self.db.insert_member(name, member_id, email, phone, join_date)
            messagebox.showinfo("Success", "Member added successfully")
            self.clear_member_fields()
            self.load_members()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def update_member(self):
        selected_item = self.members_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a member to update")
            return
        
        try:
            member_id = self.members_tree.item(selected_item)['values'][0]
            name = self.member_name.get()
            member_id_text = self.member_id.get()
            email = self.member_email.get()
            phone = self.member_phone.get()
            join_date = self.members_tree.item(selected_item)['values'][5]
            
            if not all([name, member_id_text, email, phone]):
                messagebox.showerror("Error", "Please fill all fields")
                return
            
            self.db.update_member(member_id, name, member_id_text, email, phone, join_date)
            messagebox.showinfo("Success", "Member updated successfully")
            self.clear_member_fields()
            self.load_members()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def clear_member_fields(self):
        self.member_name.delete(0, 'end')
        self.member_id.delete(0, 'end')
        self.member_email.delete(0, 'end')
        self.member_phone.delete(0, 'end')

    def select_book(self, event):
        selected_item = self.books_tree.selection()
        if selected_item:
            values = self.books_tree.item(selected_item)['values']
            self.clear_book_fields()
            self.book_title.insert(0, values[1])
            self.book_author.insert(0, values[2])
            self.book_isbn.insert(0, values[3])
            self.book_category.insert(0, values[4])
            self.book_quantity.insert(0, values[5])

    def select_member(self, event):
        selected_item = self.members_tree.selection()
        if selected_item:
            values = self.members_tree.item(selected_item)['values']
            self.clear_member_fields()
            self.member_name.insert(0, values[1])
            self.member_id.insert(0, values[2])
            self.member_email.insert(0, values[3])
            self.member_phone.insert(0, values[4])

    def load_books(self):
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)
        for book in self.db.fetch_books():
            self.books_tree.insert('', 'end', values=book)

    def load_members(self):
        for item in self.members_tree.get_children():
            self.members_tree.delete(item)
        for member in self.db.fetch_members():
            self.members_tree.insert('', 'end', values=member)

    def load_borrowings(self):
        for item in self.borrowings_tree.get_children():
            self.borrowings_tree.delete(item)
        for borrowing in self.db.fetch_borrowings():
            self.borrowings_tree.insert('', 'end', values=borrowing)

    def borrow_book_action(self):
        try:
            book_id = int(self.borrow_book.get())
            member_id = int(self.borrow_member.get())
            current_datetime = datetime.now()
            borrow_date = current_datetime.strftime("%Y-%m-%d")
            borrow_time = current_datetime.strftime("%H:%M:%S")
            return_date = (current_datetime + timedelta(days=14)).strftime("%Y-%m-%d")
            
            self.db.borrow_book(book_id, member_id, borrow_date, borrow_time, return_date)
            messagebox.showinfo("Success", "Book borrowed successfully")
            self.borrow_book.delete(0, 'end')
            self.borrow_member.delete(0, 'end')
            self.load_borrowings()
            self.load_books()
        except ValueError:
            messagebox.showerror("Error", "Invalid Book ID or Member ID")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def return_book_action(self):
        selected_item = self.borrowings_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a borrowing to return")
            return
        
        try:
            borrowing_id = self.borrowings_tree.item(selected_item)['values'][0]
            self.db.return_book(borrowing_id)
            messagebox.showinfo("Success", "Book returned successfully")
            self.load_borrowings()
            self.load_books()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_book(self):
        selected_item = self.books_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a book to delete")
            return
        
        try:
            book_id = self.books_tree.item(selected_item)['values'][0]
            title = self.books_tree.item(selected_item)['values'][1]
            
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the book '{title}'?"):
                # Check if book has active borrowings
                if self.db.is_book_borrowed(book_id):
                    messagebox.showerror("Error", "Cannot delete book with active borrowings")
                    return
                
                self.db.remove_book(book_id)
                messagebox.showinfo("Success", "Book deleted successfully")
                self.clear_book_fields()
                self.load_books()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def delete_member(self):
        selected_item = self.members_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a member to delete")
            return
        
        try:
            member_id = self.members_tree.item(selected_item)['values'][0]
            name = self.members_tree.item(selected_item)['values'][1]
            
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the member '{name}'?"):
                self.db.delete_member(member_id)
                messagebox.showinfo("Success", "Member deleted successfully")
                self.clear_member_fields()
                self.load_members()
        except Exception as e:
            messagebox.showerror("Error", str(e))

# To run the application
if __name__ == "__main__":
    app = LibraryManagementSystem()
