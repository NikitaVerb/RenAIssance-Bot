import aiosqlite


async def add_user_backup_account(user_id: int, email: str):
    # Подключаемся к базе данных
    async with aiosqlite.connect('renaissancebot.db') as conn:
        cursor = await conn.cursor()

        # Выполняем SQL-запрос для вставки данных в таблицу UserBackupAccounts
        try:
            await cursor.execute('''
                INSERT INTO UserBackupAccounts (user_id, email)
                VALUES (?, ?)
            ''', (user_id, email))

            # Фиксируем изменения в базе данных
            await conn.commit()

            return True  # Успешное выполнение
        except aiosqlite.IntegrityError:
            # Обработка ошибки, если связь уже существует или нарушены ограничения целостности
            return False  # Ошибка, связь не добавлена
