from datetime import datetime

import aiosqlite


async def get_inactive_user_count_by_email(email: str) -> int:
    async with aiosqlite.connect('../Data/renaissancebot.db') as db:
        # Получаем текущую дату
        current_date = datetime.now().date()

        # Выполняем запрос для подсчета количества пользователей с истекшими подписками
        async with db.execute('''
            SELECT COUNT(*)
            FROM Users
            INNER JOIN UserEmails ON Users.user_id = UserEmails.user_id
            WHERE UserEmails.email = ?
            AND Users.expiration_date IS NOT NULL
            AND Users.expiration_date < ?
        ''', (email, current_date)) as cursor:
            count = await cursor.fetchone()
            return count[0] if count else 0
