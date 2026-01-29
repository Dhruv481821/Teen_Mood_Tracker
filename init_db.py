import sqlite3

def init_db():
    conn = sqlite3.connect('moods.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS moods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mood INTEGER NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("Database and table created successfully!")

if __name__ == '__main__':
    init_db()
