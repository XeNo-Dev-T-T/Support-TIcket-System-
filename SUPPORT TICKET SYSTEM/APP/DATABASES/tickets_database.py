import sqlite3

DB_FILE = "tickets.db"

def init_ticket_db():
    """Safely creates the table across threads if it does not exist."""
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    db_cursor = conn.cursor()
    db_cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            user_email TEXT NOT NULL,
            bug_title TEXT NOT NULL,
            bug_description TEXT NOT NULL,
            status TEXT DEFAULT 'Open',
            solution_text TEXT DEFAULT 'No solution provided yet.'
        )
    """)
    conn.commit()
    db_cursor.close()
    conn.close()

def create_ticket(name, email, title, description):
    """Safely inserts a new bug report without thread conflicts."""
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    db_cursor = conn.cursor()
    try:
        db_cursor.execute(
            """
            INSERT INTO tickets (user_name, user_email, bug_title, bug_description) 
            VALUES (?, ?, ?, ?)
            """,
            (name, email, title, description)
        )
        conn.commit()
    finally:
        db_cursor.close()
        conn.close()

def fetch_user_tickets(email):
    """Safely retrieves user-specific bug data across threads."""
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    db_cursor = conn.cursor()
    try:
        db_cursor.execute(
            """
            SELECT id, bug_title, bug_description, status, solution_text 
            FROM tickets 
            WHERE user_email = ? 
            ORDER BY id DESC
            """,
            (email,)
        )
        tickets = db_cursor.fetchall()
        return tickets
    finally:
        db_cursor.close()
        conn.close()

def update_ticket_solution(ticket_id, solution):
    """Safely overwrites and resolves a ticket across threads."""
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    db_cursor = conn.cursor()
    try:
        db_cursor.execute(
            """
            UPDATE tickets 
            SET solution_text = ?, status = 'Resolved' 
            WHERE id = ?
            """,
            (solution, ticket_id)
        )
        conn.commit()
    finally:
        db_cursor.close()
        conn.close()
