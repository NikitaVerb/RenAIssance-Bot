import aiosqlite


async def update_user_email(user_id, new_email):
    async with aiosqlite.connect('renaissancebot.db') as conn:
        cursor = await conn.cursor()
        await cursor.execute('''UPDATE Users SET email = ? WHERE user_id = ?''', (new_email, user_id))
        await conn.commit()
