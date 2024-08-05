import aiosqlite


async def check_user_in_db(user_id: int) -> bool:
    async with aiosqlite.connect('renaissancebot.db') as db:
        async with db.execute('''SELECT email FROM Users WHERE user_id = ?''', (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row is not None



