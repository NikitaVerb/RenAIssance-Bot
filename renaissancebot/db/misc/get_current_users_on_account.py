from datetime import datetime

import aiosqlite


async def get_current_users_on_account(email: str):
    async with aiosqlite.connect('../Data/renaissancebot.db') as conn:
        cursor = await conn.cursor()

        # Текущая дата
        current_date = datetime.now().date()

        # SQL-запрос для получения пользователей с expiration_date < текущая дата
        query = '''
            SELECT Users.user_id
            FROM Users
            INNER JOIN UserEmails ON Users.user_id = UserEmails.user_id
            WHERE UserEmails.email = ? AND Users.expiration_date > ?
        '''

        # Выполняем запрос с подставленным значением email и текущей датой
        await cursor.execute(query, (email, current_date))

        # Получаем все результаты
        expired_users = await cursor.fetchall()

        return expired_users


