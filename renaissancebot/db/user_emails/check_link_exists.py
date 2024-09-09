import aiosqlite


async def check_link_exists(user_id: int, email_account: str) -> bool:
    async with aiosqlite.connect('../Data/renaissancebot.db') as db:
        async with db.execute('''
            SELECT 1 FROM UserEmails 
            WHERE user_id = ? AND email = ?
        ''', (user_id, email_account)) as cursor:
            row = await cursor.fetchone()
            return row is not None
