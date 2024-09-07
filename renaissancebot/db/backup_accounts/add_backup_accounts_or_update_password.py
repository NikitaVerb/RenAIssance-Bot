import aiosqlite


async def add_backup_account_or_update_password(email: str, password: str):
    # Подключаемся к базе данных
    async with aiosqlite.connect('renaissancebot.db') as db:
        # Выполняем SQL запрос на добавление аккаунта в таблицу BackupAccounts
        await db.execute('''
            INSERT INTO BackupAccounts (email, password)
            VALUES (?, ?)
            ON CONFLICT(email) DO UPDATE SET password=excluded.password
        ''', (email, password))

        # Сохраняем изменения в базе данных
        await db.commit()
