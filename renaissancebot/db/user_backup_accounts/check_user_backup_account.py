import aiosqlite


async def check_user_backup_account(user_id: int) -> bool:
    async with aiosqlite.connect('../Data/renaissancebot.db') as conn:
        cursor = await conn.cursor()

        # Выполняем запрос на проверку существования записи по user_id
        await cursor.execute('''
            SELECT 1 FROM UserBackupAccounts WHERE user_id = ?
        ''', (user_id,))

        # Извлекаем одну строку результата, если она существует
        result = await cursor.fetchone()

        # Если строка найдена, возвращаем True, иначе False
        return result is not None