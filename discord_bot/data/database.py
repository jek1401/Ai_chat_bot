import sys
import os

# Добавляем родительскую директорию в sys.path, чтобы Python мог найти config.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Теперь можно импортировать конфиг
from tgbot.config import DB_PATH  # Путь к базе данных из config.py
from tgbot.config import active_sessions

# Остальной код работы с БД
import sqlite3

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
            personality TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()  # Инициализация базы данных



def register_user(name, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (name, password, points) VALUES (?, ?, 0)", (name, password))
        conn.commit()
        return "✅ Регистрация прошла успешно!"
    except sqlite3.IntegrityError:
        return "❌ Имя пользователя уже занято."
    finally:
        conn.close()

def login_user(author_id, name, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE name = ?", (name,))
    row = c.fetchone()
    conn.close()

    if row and row[0] == password:
        active_sessions[author_id] = name
        return True
    return False
