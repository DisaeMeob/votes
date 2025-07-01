import sqlite3

def create_table():
    conn = sqlite3.connect('votes.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS votes(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER UNIQUE, option TEXT)''')
    conn.commit()
    conn.close()

def add_vote(user_id, option):
    conn = sqlite3.connect('votes.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''INSERT INTO votes(user_id, option) VALUES (?,?)''', (user_id, option))
    except sqlite3.IntegrityError:
        pass
    conn.commit()
    conn.close()

def count_votes():
    conn = sqlite3.connect('votes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT option, COUNT(*) FROM votes GROUP BY option ')
    result = cursor.fetchall()
    conn.close()
    return result