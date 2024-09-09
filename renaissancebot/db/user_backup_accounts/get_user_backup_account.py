import aiosqlite


async def get_user_backup_account(user_id: int) -> str:
    async with aiosqlite.connect('../Data/renaissancebot.db') as db:
        async with db.execute('''SELECT email FROM UserBackupAccounts WHERE user_id = ?''', (user_id,)) as cursor:
            row = await cursor.fetchone()
            if row is not None:
                return row[0]
