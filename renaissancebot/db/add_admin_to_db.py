import aiosqlite


async def add_admin_to_db(user_id: int):
    async with aiosqlite.connect('renaissancebot.db') as conn:
        cursor = await conn.cursor()
        await cursor.execute('''INSERT INTO Admins (user_id) VALUES (?)''', (user_id,))
        await conn.commit()
        await cursor.close()
