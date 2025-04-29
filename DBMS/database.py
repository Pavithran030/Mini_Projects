import sqlite3
import os

class Database:
    def __init__(self, db):
        db_exists = os.path.exists(db)
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        
        if db_exists:
            self.cur.execute("DROP TABLE IF EXISTS borrowings")
            self.cur.execute("DROP TABLE IF EXISTS members")
            self.cur.execute("DROP TABLE IF EXISTS books")
            self.con.commit()
        
        # books table
        sql = """
        CREATE TABLE IF NOT EXISTS books(
            id Integer Primary Key,
            title text,
            author text,
            isbn text,
            category text,
            quantity integer,
            available integer
        )
        """
        self.cur.execute(sql)
        self.con.commit()

        #members table
        sql_members = """
        CREATE TABLE IF NOT EXISTS members(
            id Integer Primary Key,
            name text,
            member_id text,
            email text,
            phone text,
            join_date text
        )
        """
        self.cur.execute(sql_members)
        self.con.commit()

        # borrowings table
        # Create borrowings table with time field
        sql_borrowings = """
        CREATE TABLE IF NOT EXISTS borrowings(
            id Integer Primary Key,
            book_id integer,
            member_id integer,
            borrow_date text,
            borrow_time text,
            return_date text,
            status text,
            FOREIGN KEY (book_id) REFERENCES books (id),
            FOREIGN KEY (member_id) REFERENCES members (id)
        )
        """
        self.cur.execute(sql_borrowings)
        self.con.commit()

    # Book operations
    def insert_book(self, title, author, isbn, category, quantity):
        self.cur.execute("insert into books values (NULL,?,?,?,?,?,?)",
                        (title, author, isbn, category, quantity, quantity))
        self.con.commit()

    def fetch_books(self):
        self.cur.execute("SELECT * from books")
        return self.cur.fetchall()

    def is_book_borrowed(self, book_id):
        """Check if a book is currently borrowed"""
        self.cur.execute("SELECT COUNT(*) FROM borrowings WHERE book_id=? AND status='Borrowed'", (book_id,))
        result = self.cur.fetchone()
        return result[0] > 0

    def remove_book(self, id):
        # Check if book has any active borrowings
        if self.is_book_borrowed(id):
            raise Exception("Cannot delete book with active borrowings")
        
        self.cur.execute("delete from books where id=?", (id,))
        self.con.commit()

    def update_book(self, id, title, author, isbn, category, quantity):
        self.cur.execute(
            "update books set title=?, author=?, isbn=?, category=?, quantity=?, available=? where id=?",
            (title, author, isbn, category, quantity, quantity, id))
        self.con.commit()

    # Member operations
    def insert_member(self, name, member_id, email, phone, join_date):
        self.cur.execute("insert into members values (NULL,?,?,?,?,?)",
                        (name, member_id, email, phone, join_date))
        self.con.commit()

    def fetch_members(self):
        self.cur.execute("SELECT * from members")
        return self.cur.fetchall()

    def remove_member(self, id):
        self.cur.execute("delete from members where id=?", (id,))
        self.con.commit()

    def update_member(self, id, name, member_id, email, phone, join_date):
        self.cur.execute(
            "update members set name=?, member_id=?, email=?, phone=?, join_date=? where id=?",
            (name, member_id, email, phone, join_date, id))
        self.con.commit()

    # Borrowing operations
    def borrow_book(self, book_id, member_id, borrow_date, borrow_time, return_date):
        self.cur.execute("insert into borrowings values (NULL,?,?,?,?,?,?)",
                        (book_id, member_id, borrow_date, borrow_time, return_date, "Borrowed"))
        self.cur.execute("update books set available=available-1 where id=?", (book_id,))
        self.con.commit()

    def return_book(self, borrowing_id):
        self.cur.execute("update borrowings set status='Returned' where id=?", (borrowing_id,))
        self.cur.execute("update books set available=available+1 where id=(select book_id from borrowings where id=?)", (borrowing_id,))
        self.con.commit()

    def fetch_borrowings(self):
        self.cur.execute("""
            SELECT b.id, books.title, members.name, b.borrow_date, b.borrow_time, b.return_date, b.status 
            FROM borrowings b
            JOIN books ON b.book_id = books.id
            JOIN members ON b.member_id = members.id
        """)
        return self.cur.fetchall()
    
    def delete_book(self, book_id):
        # Check if book has any active borrowings
        self.cur.execute("SELECT COUNT(*) FROM borrowings WHERE book_id=? AND status='Borrowed'", (book_id,))
        active_borrowings = self.cur.fetchone()[0]
        
        if active_borrowings > 0:
            raise Exception("Cannot delete book with active borrowings")
        
        self.cur.execute("DELETE FROM books WHERE id=?", (book_id,))
        self.conn.commit()
    
    def delete_member(self, member_id):
        # Check if member has any active borrowings
        self.cur.execute("SELECT COUNT(*) FROM borrowings WHERE member_id=? AND status='Borrowed'", (member_id,))
        active_borrowings = self.cur.fetchone()[0]
        
        if active_borrowings > 0:
            raise Exception("Cannot delete member with active borrowings")
        
        self.cur.execute("DELETE FROM members WHERE id=?", (member_id,))
        self.conn.commit()
    
    def is_book_borrowed(self, book_id):
        """Check if a book is currently borrowed"""
        self.cursor.execute("SELECT COUNT(*) FROM borrowings WHERE book_id=? AND status='Borrowed'", (book_id,))
        result = self.cursor.fetchone()
        return result[0] > 0
        
