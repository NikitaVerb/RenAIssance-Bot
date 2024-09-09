import aiosqlite


async def is_backup_account(email: str) -> bool:
    # Открываем асинхронное соединение с базой данных
    async with aiosqlite.connect('../Data/renaissancebot.db') as db:
        # Выполняем запрос, чтобы проверить, существует ли указанный email в таблице резервных аккаунтов
        async with db.execute("SELECT 1 FROM BackupAccounts WHERE email = ?", (email,)) as cursor:
            result = await cursor.fetchone()

            # Если результат не пустой, значит аккаунт является резервным
            return result is not None
