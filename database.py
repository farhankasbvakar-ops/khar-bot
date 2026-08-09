import sqlite3

DB_NAME = "kharbot.db"

db = sqlite3.connect(DB_NAME, check_same_thread=False)
db.row_factory = sqlite3.Row

def init_db():
    db.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        name TEXT DEFAULT '',
        coins INTEGER DEFAULT 0,
        total_aar INTEGER DEFAULT 0,
        level INTEGER DEFAULT 1,
        job TEXT DEFAULT 'بیکار',
        profile_private INTEGER DEFAULT 0,

        pet_name TEXT DEFAULT 'کره خر',
        pet_level INTEGER DEFAULT 1,
        pet_food REAL DEFAULT 0,
        pet_last_income INTEGER DEFAULT 0,

        normal_carrot INTEGER DEFAULT 0,
        big_carrot INTEGER DEFAULT 0,
        gold_carrot INTEGER DEFAULT 0,
        legendary_carrot INTEGER DEFAULT 0,

        hook_level INTEGER DEFAULT 1,
        transfer_last INTEGER DEFAULT 0,

        jail_until INTEGER DEFAULT 0,
        spam_count INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS groups (
        chat_id INTEGER PRIMARY KEY,
        treasury INTEGER DEFAULT 0,
        total_aar INTEGER DEFAULT 0,
        rescue_event INTEGER DEFAULT 0,
        rescue_attempts INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS factories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT,
        level INTEGER DEFAULT 1,
        income INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS street_donkeys (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner_id INTEGER,
        level INTEGER DEFAULT 1,
        status TEXT DEFAULT 'آزاد'
    );
    """)

    db.commit()


def get_user(user_id, name="بازیکن"):
    user = db.execute(
        "SELECT * FROM users WHERE user_id=?",
        (user_id,)
    ).fetchone()

    if not user:
        db.execute(
            "INSERT INTO users(user_id,name) VALUES(?,?)",
            (user_id, name)
        )
        db.commit()

        user = db.execute(
            "SELECT * FROM users WHERE user_id=?",
            (user_id,)
        ).fetchone()

    return user


def update_user(user_id, **values):
    if not values:
        return

    fields = ", ".join(f"{key}=?" for key in values)

    db.execute(
        f"UPDATE users SET {fields} WHERE user_id=?",
        (*values.values(), user_id)
    )

    db.commit()


def get_group(chat_id):
    group = db.execute(
        "SELECT * FROM groups WHERE chat_id=?",
        (chat_id,)
    ).fetchone()

    if not group:
        db.execute(
            "INSERT INTO groups(chat_id) VALUES(?)",
            (chat_id,)
        )
        db.commit()

        group = db.execute(
            "SELECT * FROM groups WHERE chat_id=?",
            (chat_id,)
        ).fetchone()

    return group


def add_group_money(chat_id, amount):
    get_group(chat_id)

    db.execute(
        "UPDATE groups SET treasury=treasury+? WHERE chat_id=?",
        (amount, chat_id)
    )

    db.commit()
