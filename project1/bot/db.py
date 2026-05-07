import sqlite3

DB_NAME = 'users.db'


def connect():
    return sqlite3.connect(DB_NAME)


def create_table():
    with connect() as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS users (
            tg_id INTEGER PRIMARY KEY,
            full_name TEXT,
            phone TEXT,
            lat REAL,
            lon REAL
        )
        """)

        con.execute("""
        CREATE TABLE IF NOT EXISTS categories(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            emoji TEXT
        )
        """)

        con.execute("""
        CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER,
            name TEXT,
            price INTEGER,
            description TEXT,
            image TEXT,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
        """)



def add_user(tg_id, full_name, phone, lat, lon):
    with connect() as con:
        con.execute("""
        INSERT OR REPLACE INTO users
        (tg_id, full_name, phone, lat, lon)
        VALUES (?, ?, ?, ?, ?)
        """, (tg_id, full_name, phone, lat, lon))


def get_user(tg_id):
    with connect() as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE tg_id=?", (tg_id,))
        return cur.fetchone()


def update_name(tg_id, full_name):
    with connect() as con:
        con.execute("UPDATE users SET full_name=? WHERE tg_id=?",
                    (full_name, tg_id))


def update_phone(tg_id, phone):
    with connect() as con:
        con.execute("UPDATE users SET phone=? WHERE tg_id=?",
                    (phone, tg_id))


def add_category(name, emoji):
    with connect() as con:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO categories (name, emoji) VALUES(?, ?)",
            (name, emoji)
        )


def get_category():
    with connect() as con:
        cur = con.cursor()
        cur.execute(
            "SELECT id, name, emoji FROM categories"
        )
        return cur.fetchall()


def add_products(category_id, name, price, description, image):
    with connect() as con:
        con.execute("INSERT INTO products (category_id, name, price, description, image) VALUES (?, ?, ?, ?, ?)", (category_id, name, price, description, image))

def get_products_by_category(category_id):
    with connect() as con:
        cur = con.cursor()
        cur.execute("SELECT name, price, description, image FROM products WHERE category_id=?",
                    (category_id,))
        return cur.fetchall()







