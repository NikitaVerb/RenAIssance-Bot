import aiosqlite


async def get_all_admin_ids():
    async with aiosqlite.connect('../Data/renaissancebot.db') as conn:
        cursor = await conn.cursor()

        # Выполняем запрос для получения всех admin_id из таблицы Admins
        await cursor.execute('SELECT user_id FROM Admins')

        # Получаем все результаты
        rows = await cursor.fetchall()

        # Извлекаем список user_id
        admin_ids = [row[0] for row in rows]

    return admin_ids
