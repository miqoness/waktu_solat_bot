import sqlite3
from config import DATABASE_PATH

def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            language TEXT DEFAULT 'ms',
            zone TEXT,
            latitude REAL,
            longitude REAL,
            calculation_method INTEGER DEFAULT 20
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized and updated successfully")

def get_db_connection():
    return sqlite3.connect(DATABASE_PATH)

def update_user_location(user_id, lat=None, lon=None, zone=None):
    conn = get_db_connection()
    c = conn.cursor()
    if zone:
        c.execute("INSERT OR REPLACE INTO users (user_id, zone, latitude, longitude) VALUES (?, ?, NULL, NULL)", (user_id, zone))
    else:
        c.execute("INSERT OR REPLACE INTO users (user_id, zone, latitude, longitude) VALUES (?, NULL, ?, ?)", (user_id, lat, lon))
    conn.commit()
    conn.close()

def update_user_method(user_id, method):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO users (user_id, calculation_method) VALUES (?, ?)", (user_id, method))
    conn.commit()
    conn.close()

def update_user_language(user_id, language):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO users (user_id, language) VALUES (?, ?)", (user_id, language))
    conn.commit()
    conn.close()

# Fungsi lain yang mungkin anda sudah ada...