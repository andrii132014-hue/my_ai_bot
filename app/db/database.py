import sqlite3

def init_db():
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    # Створюємо таблицю, якщо її ще немає
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_text TEXT,
            ai_response TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_message(user_text, ai_response):
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO messages (user_text, ai_response) VALUES (?, ?)', 
                   (user_text, ai_response))
    conn.commit()
    conn.close()