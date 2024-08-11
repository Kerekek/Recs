import sqlite3

def init_db():
    con = sqlite3.connect("Recs_of_D.db")
    cur = con.cursor()
    return con, cur

def create_animetable(cur,con):
    cur.execute('CREATE TABLE IF NOT EXISTS movietable(username TEXT, title TEXT, rating INTEGER, state INTEGER)')
    con.commit()

def add_animedata(cur,con, username, title, rating, state):
    cur.execute('INSERT INTO movietable(username, title, rating, state) VALUES (?, ?, ?, ?)', (username, title, rating, state))
    con.commit()

def show_user_list(cur, username):
    cur.execute('SELECT * FROM movietable WHERE username =?', (username,))
    return cur.fetchall()

def registered_title_check(cur, username, title):
    cur.execute('SELECT * FROM movietable WHERE username =? AND title =?', (username, title))
    return cur.fetchall()

def create_usertable(cur):
    cur.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, email TEXT, password TEXT)')
    
def add_userdata(cur,con, username, email, password):
    cur.execute('INSERT INTO userstable(username, email, password) VALUES (?, ?, ?)', (username, email, password))
    con.commit()

def login_user(cur, username, password):
    cur.execute('SELECT * FROM userstable WHERE username =? AND password =? ', (username, password))
    return cur.fetchall()

def view_all_users(cur):
    cur.execute('SELECT * FROM userstable')
    return cur.fetchall()