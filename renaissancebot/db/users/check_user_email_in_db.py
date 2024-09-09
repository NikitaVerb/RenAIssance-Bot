import aiosqlite


async def check_user_email_in_db(email: str) -> bool:
    async with aiosqlite.connect('../Data/renaissancebot.db') as db:
        async with db.execute('''SELECT email FROM Users WHERE email = ?''', (email,)) as cursor:
            row = await cursor.fetchone()
            return row is not None
