import sqlite3
from datetime import datetime, timedelta
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
            pre_notification INTEGER DEFAULT 0
        )
    ''')

    try:
        c.execute("ALTER TABLE users ADD COLUMN pre_notification INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass

    c.execute('''
        CREATE TABLE IF NOT EXISTS prayer_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            prayer_name TEXT,
            prayer_date TEXT,
            logged_at TEXT,
            UNIQUE(user_id, prayer_name, prayer_date),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
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
    c.execute(
        "INSERT INTO users (user_id, zone, latitude, longitude) VALUES (?, ?, ?, ?) "
        "ON CONFLICT(user_id) DO UPDATE SET zone=excluded.zone, latitude=excluded.latitude, longitude=excluded.longitude",
        (user_id, zone, lat, lon))
    conn.commit()
    conn.close()


def update_user_language(user_id, language):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO users (user_id, language) VALUES (?, ?) "
        "ON CONFLICT(user_id) DO UPDATE SET language=excluded.language",
        (user_id, language))
    conn.commit()
    conn.close()


def update_user_pre_notification(user_id, minutes):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO users (user_id, pre_notification) VALUES (?, ?) "
        "ON CONFLICT(user_id) DO UPDATE SET pre_notification=excluded.pre_notification",
        (user_id, minutes))
    conn.commit()
    conn.close()


def get_user_pre_notification(user_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT pre_notification FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result and result[0] else 0


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


def log_prayer(user_id, prayer_name, prayer_date):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        "INSERT OR IGNORE INTO prayer_logs (user_id, prayer_name, prayer_date, logged_at) VALUES (?, ?, ?, ?)",
        (user_id, prayer_name, prayer_date, datetime.now().isoformat()))
    inserted = c.rowcount > 0
    conn.commit()
    conn.close()
    return inserted


def get_today_prayers(user_id, today):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT prayer_name FROM prayer_logs WHERE user_id = ? AND prayer_date = ?", (user_id, today))
    results = c.fetchall()
    conn.close()
    return [r[0] for r in results]


def get_prayer_stats(user_id):
    conn = get_db_connection()
    c = conn.cursor()

    c.execute("""
        SELECT prayer_date, COUNT(DISTINCT prayer_name) as count
        FROM prayer_logs
        WHERE user_id = ?
        GROUP BY prayer_date
        ORDER BY prayer_date DESC
    """, (user_id,))
    daily_results = c.fetchall()

    streak = 0
    today = datetime.now().strftime('%Y-%m-%d')
    expected_date = today

    for date, count in daily_results:
        if date == expected_date and count >= 5:
            streak += 1
            prev = datetime.strptime(expected_date, '%Y-%m-%d') - timedelta(days=1)
            expected_date = prev.strftime('%Y-%m-%d')
        else:
            break

    c.execute("SELECT COUNT(*) FROM prayer_logs WHERE user_id = ?", (user_id,))
    total = c.fetchone()[0]

    c.execute("""
        SELECT COUNT(*) FROM prayer_logs
        WHERE user_id = ? AND prayer_date >= ?
    """, (user_id, (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')))
    week_total = c.fetchone()[0]

    c.execute("""
        SELECT COUNT(*) FROM prayer_logs
        WHERE user_id = ? AND prayer_date >= ?
    """, (user_id, (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')))
    month_total = c.fetchone()[0]

    conn.close()

    return {
        'streak': streak,
        'total': total,
        'week_total': week_total,
        'month_total': month_total,
    }
