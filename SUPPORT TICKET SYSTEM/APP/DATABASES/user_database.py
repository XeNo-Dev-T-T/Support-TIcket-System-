import sqlite3

def save_user(name, email):
    # Open a completely fresh connection and cursor INSIDE the function
    conn = sqlite3.connect("user_data.db")
    db_cursor = conn.cursor()  # Renamed to db_cursor to avoid global conflicts
    
    try:
        db_cursor.execute(
            "INSERT INTO users (user_name, user_email) VALUES (?, ?)", 
            (name, email)
        )
        conn.commit()
        print(f"Successfully saved: {name}")
    except sqlite3.IntegrityError:
        print("Email already exists!")
    finally:
        # Close everything before leaving the function
        db_cursor.close()
        conn.close()
