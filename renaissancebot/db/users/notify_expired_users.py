from datetime import datetime
import aiosqlite


async def notify_expired_users():
    async with aiosqlite.connect('renaissancebot.db') as conn:
        cursor = await conn.cursor()

        # Текущая дата
        current_date = datetime.now().date()

        # Выбираем пользователей с истекшей подпиской и у которых notified = 0
        await cursor.execute('''
            SELECT user_id
            FROM Users
            WHERE expiration_date <= ? AND notified = 0
        ''', (current_date,))

        # Получаем всех пользователей с истекшей подпиской
        expired_users = await cursor.fetchall()

        if expired_users:
            # Обновляем notified для всех найденных пользователей на 1
            user_ids = [user[0] for user in expired_users]
            await cursor.executemany('''
                UPDATE Users
                SET notified = 1
                WHERE user_id = ?
            ''', [(user_id,) for user_id in user_ids])

            # Применяем изменения
            await conn.commit()

        return expired_users  # Возвращаем список user_id для дальнейшего использования
