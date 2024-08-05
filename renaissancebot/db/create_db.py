import aiosqlite


async def create_db():
    async with aiosqlite.connect('renaissancebot.db') as conn:
        cursor = await conn.cursor()
        await cursor.execute('''CREATE TABLE IF NOT EXISTS Users(
                          user_id  INTEGER PRIMARY KEY,
                          email  TEXT)''')
        await conn.commit()
