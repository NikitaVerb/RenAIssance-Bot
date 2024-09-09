import aiosqlite


# Функция для установки даты покупки
async def set_purchase_date(user_id: int, purchase_date: str):
    async with aiosqlite.connect('../Data/renaissancebot.db') as db:
        await db.execute('''
            UPDATE Users
            SET purchase_date = ?
            WHERE user_id = ?
        ''', (purchase_date, user_id))
        await db.commit()
