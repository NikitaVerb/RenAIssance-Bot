import aiosqlite


async def get_used_backup_account_date(user_id: int) -> str:
    async with aiosqlite.connect('renaissancebot.db') as db:
        async with db.execute('''SELECT used_backup_account FROM Users WHERE user_id = ?''', (user_id,)) as cursor:
            row = await cursor.fetchone()
            if row is not None:
                return row[0]
