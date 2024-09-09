from datetime import date

import aiosqlite


async def set_backup_account_date(user_id: int, backup_date: str):
    # Подключаемся к базе данных
    async with aiosqlite.connect('../Data/renaissancebot.db') as conn:
        cursor = await conn.cursor()

        # Выполняем SQL-запрос для обновления даты в таблице UserBackupAccounts
        try:
            await cursor.execute('''
                UPDATE Users
                SET used_backup_account = ?
                WHERE user_id = ?
            ''', (backup_date, user_id,))

            # Фиксируем изменения в базе данных
            await conn.commit()

            return True  # Успешное выполнение
        except aiosqlite.IntegrityError:
            # Обработка ошибки, если связь не существует или нарушены ограничения целостности
            return False  # Ошибка, дата не установлена
