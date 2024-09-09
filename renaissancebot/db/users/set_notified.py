# Функция для установки даты окончания подписки
import aiosqlite


async def set_notified(user_id: int, notified: int):
    async with aiosqlite.connect('../Data/renaissancebot.db') as db:
        await db.execute('''
            UPDATE Users
            SET notified = ?
            WHERE user_id = ?
        ''', (notified, user_id))
        await db.commit()
