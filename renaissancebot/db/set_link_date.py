import aiosqlite


# Функция для установки даты покупки
async def set_link_date(user_id: int, link: str):
    async with aiosqlite.connect('renaissancebot.db') as db:
        await db.execute('''
            UPDATE UserBackupAccounts
            SET link_date = ?
            WHERE user_id = ?
        ''', (link, user_id))
        await db.commit()
