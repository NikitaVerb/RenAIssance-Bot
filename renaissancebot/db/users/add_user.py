import aiosqlite


async def add_user(user_id, email):
    async with aiosqlite.connect('renaissancebot.db') as conn:
        cursor = await conn.cursor()
        await cursor.execute('''INSERT INTO Users (user_id, email) VALUES (?, ?)''', (user_id, email))
        await conn.commit()
