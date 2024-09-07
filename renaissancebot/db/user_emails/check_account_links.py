import aiosqlite


async def check_account_links(email: str) -> bool:
    async with aiosqlite.connect('renaissancebot.db') as db:
        # Проверяем наличие связей с указанным email в таблице UserEmails
        async with db.execute('SELECT COUNT(*) FROM UserEmails WHERE email = ?', (email,)) as cursor:
            result = await cursor.fetchone()
            # Возвращает True, если связи существуют, иначе False
            return result[0] > 0
