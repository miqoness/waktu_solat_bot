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
            longitude REAL
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
        c.execute("INSERT OR REPLACE INTO users (user_id, zone, latitude, longitude) VALUES (?, ?, ?, ?)", (user_id, zone, lat, lon))
    else:
        c.execute("INSERT OR REPLACE INTO users (user_id, zone, latitude, longitude) VALUES (?, NULL, ?, ?)", (user_id, lat, lon))
    conn.commit()
    conn.close()

def update_user_language(user_id, language):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO users (user_id, language) VALUES (?, ?)", (user_id, language))
    conn.commit()
    conn.close()

def get_user_zone(user_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT zone FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def get_user_location(user_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT latitude, longitude FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result if result else (None, None)

def get_user_location_info(user_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT zone, latitude, longitude FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result if result else (None, None, None)