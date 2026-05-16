import sqlite3

DB_NAME = 'taxi.db'

def connect():
    return sqlite3.connect(DB_NAME)

def create_table():
    with connect() as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS users(
            telegram_id INTEGER PRIMARY KEY,
            full_name TEXT,
            phone TEXT
        )
        """)

        con.execute("""
        CREATE TABLE IF NOT EXISTS drivers(
            telegram_id INTEGER PRIMARY KEY,
            full_name TEXT,
            phone TEXT,
            lat REAL,
            lon REAL,
            car_name TEXT,
            car_plate_number TEXT,
            car_color TEXT,
            is_active INTEGER
        )
        """)

        con.execute("""
        CREATE TABLE IF NOT EXISTS orders(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            driver_id INTEGER,
            from_loc TEXT,
            to_loc TEXT,
            rejected_drivers TEXT DEFAULT '',
            progress_75 INTEGER DEFAULT 0,
            progress_50 INTEGER DEFAULT 0,
            progress_25 INTEGER DEFAULT 0,
            status TEXT,
            price INTEGER,
            distance REAL,
            created_at TEXT
        )
        """)

        con.execute("""
        CREATE TABLE IF NOT EXISTS tariffs(
            id INTEGER PRIMARY KEY,
            name TEXT,
            base_price INTEGER,
            km_price INTEGER
        )
        """)

def add_user(telegram_id, full_name, phone):
    with connect() as con:
        con.execute("""
        INSERT OR REPLACE INTO users
        (telegram_id, full_name, phone)
        VALUES(?, ?, ?)
        """, (telegram_id, full_name, phone))

def add_driver(telegram_id, full_name, phone, lat, lon, car_name, car_plate_number, car_color, is_active):
    with connect() as con:
        con.execute("""
        INSERT OR REPLACE INTO drivers
        (telegram_id, full_name, phone, lat, lon, car_name, car_plate_number, car_color, is_active)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (telegram_id, full_name, phone, lat, lon, car_name, car_plate_number, car_color, is_active))


def get_user(telegram_id):
    with connect() as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE telegram_id=?", (telegram_id,))
        return cur.fetchone()

def create_order(user_id, from_loc, to_loc, price, distance, created_at):
    with connect() as con:
        cur = con.cursor()
        cur.execute("""
            INSERT INTO orders (user_id, from_loc, to_loc, price, distance, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, from_loc, to_loc, price, distance, created_at))
        return cur.lastrowid


def get_active_drivers():
    with connect() as con:
        cur = con.cursor()
        cur.execute("SELECT telegram_id, lat, lon FROM drivers WHERE is_active=1", )
        return cur.fetchall()

def update_driver_location(telegram_id, lat, lon):
    with connect() as con:
        cur = con.cursor()
        cur.execute("""UPDATE drivers SET lat=?, lon=? WHERE telegram_id=?""", (lat, lon, telegram_id))

def get_last_order_by_driver(driver_id):
    with connect() as con:
        cur = con.cursor()
        cur.execute("""SELECT id, user_id, from_loc, to_loc, distance FROM orders WHERE driver_id=? ORDER BY id DESC LIMIT 1""", (driver_id,))
        row = cur.fetchone()

        if not row:
            return None

        return {
            "id": row[0],
            "user_id": row[1],
            "from_loc": row[2],
            "to_loc": row[3],
            "distance": row[4]
        }

def get_driver(telegram_id):
    with connect() as con:
        cur = con.cursor()
        cur.execute("""SELECT full_name, phone FROM drivers WHERE telegram_id=? """,
                    (telegram_id, ))
        return cur.fetchone()

def mark_progress(order_id, field):
    with connect() as con:
        con.execute(f"""UPDATE orders SET {field}=1 WHERE id=?""", (order_id,))

def assign_driver(order_id, driver_id):
    with connect() as con:
        con.execute("""
        UPDATE orders SET driver_id=? WHERE id=?
        """, (driver_id, order_id))

def add_rejected_driver(order_id, driver_id):
    with connect() as con:
        cur = con.cursor()

        cur.execute("SELECT rejected_drivers FROM orders WHERE id=?", (order_id,))
        current = cur.fetchone()[0] or ""

        updated = current + f"{driver_id},"

        cur.execute(
            "UPDATE orders SET rejected_drivers=? WHERE id=?",
            (updated, order_id)
        )

def get_available_drivers(rejected_ids):
    with connect() as con:
        cur = con.cursor()
        if not rejected_ids:
            cur.execute("SELECT telegram_id, lat, lon FROM drivers WHERE is_active=1")
            return cur.fetchall()
        placeholders = ",".join("?" * len(rejected_ids))
        query = f"""SELECT telegram_id, lat, lon FROM drivers WHERE is_active=1 AND telegram_id NOT IN ({placeholders})"""
        cur.execute(query, rejected_ids)
        return cur.fetchall()

def get_rejected_drivers(order_id):
    with connect() as con:
        cur = con.cursor()
        cur.execute("SELECT rejected_drivers FROM orders WHERE id=?", (order_id,))
        row = cur.fetchone()
        return row[0] if row else ""

def update_order_status(order_id, status):
    with connect() as con:
        con.execute(
            "UPDATE orders SET status=? WHERE id=?",
            (status, order_id)
        )

def get_order(user_id):
    with connect() as con:
        cur = con.cursor()
        cur.execute("SELECT id, from_loc, to_loc, driver_id, distance, price, created_at FROM orders WHERE user_id=? ORDER BY id DESC", (user_id, ))
        return cur.fetchall()

def count_driver():
    with connect() as con:
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM drivers")
        return cur.fetchall()

def count_user():
    with connect() as con:
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM users")
        return cur.fetchall()

def get_last_10_orders():
    with connect() as con:
        cur = con.cursor()
        cur.execute("SELECT id, from_loc, to_loc, driver_id, distance, price, created_at FROM orders ORDER BY id ASC LIMIT 10")
        return cur.fetchmany(10)

def add_tariff(name, base_price, km_price):
    with connect() as con:
        con.execute("""INSERT OR REPLACE INTO tariffs
                    (name, base_price, km_price) 
                    VALUES(?, ?, ?) 
                    """,
                    (name, base_price, km_price))

def get_tariff(name):
    with connect() as con:
        cur = con.cursor()
        cur.execute(
            "SELECT * FROM tariffs WHERE name=?",
            (name,)
        )
        return cur.fetchone()

def get_tariffs():
    with connect() as con:
        cur = con.cursor()
        cur.execute("SELECT id, name, base_price, km_price FROM tariffs ORDER BY id DESC", ())
        return cur.fetchall()