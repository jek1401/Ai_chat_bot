import sqlite3
import os
from datetime import datetime, timedelta
from config import DB_PATH

active_sessions = {}

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(""" 
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            points INTEGER DEFAULT 0,
            voice TEXT,
            personality TEXT,
            last_points_update TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def register_user(name, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (name, password, points, last_points_update) VALUES (?, ?, 0, ?)", 
                 (name, password, datetime.now()))
        conn.commit()
        return True, "✅ Регистрация прошла успешно!"
    except sqlite3.IntegrityError:
        return False, "❌ Имя пользователя уже занято."
    finally:
        conn.close()

def login_user(user_id, name, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE name = ?", (name,))
    row = c.fetchone()
    conn.close()

    if row and row[0] == password:
        active_sessions[user_id] = name
        return True
    return False

def update_points():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now()
    c.execute("SELECT id, last_points_update FROM users")
    users = c.fetchall()
    
    for user_id, last_update in users:
        if last_update:
            last_update = datetime.strptime(last_update, "%Y-%m-%d %H:%M:%S.%f")
            if now - last_update >= timedelta(minutes=5):
                c.execute("UPDATE users SET points = points + 1, last_points_update = ? WHERE id = ?", 
                         (now, user_id))
    
    conn.commit()
    conn.close()

def get_user_data(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    username = active_sessions.get(user_id)
    if not username:
        return None
    
    c.execute("SELECT points, voice, personality FROM users WHERE name = ?", (username,))
    row = c.fetchone()
    conn.close()
    return row