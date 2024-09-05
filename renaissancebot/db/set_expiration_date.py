# Функция для установки даты окончания подписки
import aiosqlite


async def set_expiration_date(user_id: int, expiration_date: str):
    async with aiosqlite.connect('renaissancebot.db') as db:
        await db.execute('''
            UPDATE Users
            SET expiration_date = ?
            WHERE user_id = ?
        ''', (expiration_date, user_id))
        await db.commit()
