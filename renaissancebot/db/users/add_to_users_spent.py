# Функция для добавления суммы к полю spent
import aiosqlite


async def add_to_users_spent(user_id: int, amount: int):
    async with aiosqlite.connect('../Data/renaissancebot.db') as db:
        await db.execute('''
            UPDATE Users
            SET spent = spent + ?
            WHERE user_id = ?
        ''', (amount, user_id))
        await db.commit()