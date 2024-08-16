import aiosqlite


async def get_user_account(user_id: int) -> str:
    async with aiosqlite.connect('renaissancebot.db') as db:
        async with db.execute('''SELECT email FROM UserEmails WHERE user_id = ?''', (user_id,)) as cursor:
            row = await cursor.fetchone()
            if row is not None:
                return row[0]
