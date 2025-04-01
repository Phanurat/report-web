import sqlite3

DATABASE = "attendance.db"

def create_tables():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # สร้างตาราง users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # สร้างตาราง attendance
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            check_in TIMESTAMP,
            check_out TIMESTAMP
        )
    ''')

    # เพิ่มผู้ใช้ตัวอย่าง
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'admin123')")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("Database initialized successfully!")
