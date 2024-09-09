import aiosqlite


async def get_account_password(email):
    # Подключаемся к базе данных асинхронно
    async with aiosqlite.connect('../Data/renaissancebot.db') as db:
        # Выполняем SQL-запрос для получения пароля по email
        async with db.execute('SELECT password FROM Emails WHERE email = ?', (email,)) as cursor:
            # Извлекаем результат
            result = await cursor.fetchone()

    # Проверяем, найден ли результат, и возвращаем пароль, если да
    if result:
        return result[0]  # Пароль будет первым (и единственным) элементом в результате
    else:
        return None  # Если email не найден, возвращаем None
