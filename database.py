import sqlite3 as sql

database_name = "film_bot.db"

# VARCHAR(max_symbols=255)

async def create_tables(dp):
    con = sql.connect(database_name)
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS user(
                user_id INTEGER,
                username VARCHAR(100)
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS film(
                film_code INTEGER,
                film_name VARCHAR(100),
                film_id INTEGER
    )""")



async def create_user(user_id, username):
    con = sql.connect(database_name)
    cur = con.cursor()
    select = cur.execute(f"SELECT * FROM user WHERE user_id = ?", (user_id,)).fetchone()
    cur.execute("INSERT INTO user VALUES (?, ?)", (user_id, username))

    if not select:
        cur.execute("INSERT INTO user VALUES (?, ?)", (user_id, username))

    con.commit()


async def insert_film(film_code, film_name, film_id):
    con = sql.connect(database_name)
    cur = con.cursor()
    cur.execute("INSERT INTO film VALUES (?, ?, ?)", (film_code, film_name, film_id))

    con.commit()


async def get_film_by_code(film_code):
    con = sql.connect(database_name)
    cur = con.cursor()
    film = cur.execute(f"SELECT * FROM film WHERE film_code = ?", (film_code,)).fetchone()

    return film