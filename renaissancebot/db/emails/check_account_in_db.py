import aiosqlite


async def check_account_in_db(email: str) -> bool:
    async with aiosqlite.connect('../Data/renaissancebot.db') as db:
        async with db.execute('''SELECT email FROM Emails WHERE email = ?''', (email,)) as cursor:
            row = await cursor.fetchone()
            return row is not None
