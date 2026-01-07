import aiosqlite

DB = "neurogym.db"

async def init_db():
    async with aiosqlite.connect(DB) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            tg_id INTEGER PRIMARY KEY,
            points INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1
        )
        """)
        await db.commit()

async def get_user(tg_id):
    async with aiosqlite.connect(DB) as db:
        cur = await db.execute(
            "SELECT points, level FROM users WHERE tg_id=?",
            (tg_id,)
        )
        return await cur.fetchone()

async def add_user(tg_id):
    async with aiosqlite.connect(DB) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (tg_id) VALUES (?)",
            (tg_id,)
        )
        await db.commit()

async def update_user(tg_id, points, level):
    async with aiosqlite.connect(DB) as db:
        await db.execute(
            "UPDATE users SET points=?, level=? WHERE tg_id=?",
            (points, level, tg_id)
        )
        await db.commit()
