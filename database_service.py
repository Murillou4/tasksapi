import sqlite3 as sql
from threading import local

class DatabaseService:
    _thread_local = local()
    
    def __init__(self):
        self._init_connection()
        self.create_tables()

    def _init_connection(self):
        if not hasattr(self._thread_local, 'con'):
            self._thread_local.con = sql.connect('database.db')
            self._thread_local.con.execute("PRAGMA foreign_keys = ON")
            self._thread_local.cur = self._thread_local.con.cursor()

    @property
    def con(self):
        self._init_connection()
        return self._thread_local.con

    @property
    def cur(self):
        self._init_connection()
        return self._thread_local.cur

    def create_tables(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS USERS (
            uid TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            password BLOB NOT NULL,
            photo BLOB
        )''')
        self.con.commit()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS TASKS (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            created_at TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0,
            uid TEXT NOT NULL,
            FOREIGN KEY (uid) REFERENCES USERS(uid) ON DELETE CASCADE
        )''')
        self.con.commit() 
        

    def add_task(self, topic, created_at, uid):
        self.cur.execute('''INSERT INTO TASKS (topic, created_at, uid) VALUES (?, ?, ?)''', (topic, created_at, uid))
        self.con.commit()

    def get_tasks(self, uid):
        self.cur.execute('''SELECT * FROM TASKS WHERE uid = ?''', (uid,))
        return self.cur.fetchall()
    
    def update_task_topic(self, id, topic):
        self.cur.execute('''UPDATE TASKS SET topic = ? WHERE id = ?''', (topic, id))
        self.con.commit()

    def update_task_completed(self, id, completed):
        self.cur.execute('''UPDATE TASKS SET completed = ? WHERE id = ?''', (completed, id))
        self.con.commit()

    def delete_task(self, id):
        self.cur.execute('''DELETE FROM TASKS WHERE id = ?''', (id,))
        self.con.commit()

    def create_user(self, uid, name, email, password, photo = None):
        self.cur.execute('''INSERT INTO USERS (uid, name, email, password, photo) VALUES (?, ?, ?, ?, ?)''', (uid, name, email, password, photo))
        self.con.commit()

    def get_user(self, uid):
        self.cur.execute('''SELECT * FROM USERS WHERE uid = ?''', (uid,))
        return self.cur.fetchone()
    
    def get_user_by_email(self, email):
        self.cur.execute('''SELECT * FROM USERS WHERE email = ?''', (email,))
        return self.cur.fetchone()
    
    def update_user_photo(self, uid, photo):
        self.cur.execute('''UPDATE USERS SET photo = ? WHERE uid = ?''', (photo, uid))
        self.con.commit()

    def update_user_password(self, uid, password):
        self.cur.execute('''UPDATE USERS SET password = ? WHERE uid = ?''', (password, uid))
        self.con.commit()

    def delete_user(self, uid):
        self.cur.execute('''DELETE FROM USERS WHERE uid = ?''', (uid,))
        self.con.commit()


