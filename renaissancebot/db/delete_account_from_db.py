import aiosqlite


async def delete_account_from_db(email: str) -> bool:
    async with aiosqlite.connect('renaissancebot.db') as db:
        # Удаление email из таблицы Emails
        await db.execute('DELETE FROM Emails WHERE email = ?', (email,))
        # Сохранение изменений
        await db.commit()
        # Возвращает True, если email успешно удален
        return True