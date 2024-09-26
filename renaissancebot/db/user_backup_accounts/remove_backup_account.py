import aiosqlite


async def remove_backup_account(user_id: int):
    async with aiosqlite.connect('../Data/renaissancebot.db') as conn:
        cursor = await conn.cursor()
        await cursor.execute(f'''DELETE FROM UserBackupAccounts WHERE user_id = {user_id}''')
        await conn.commit()
