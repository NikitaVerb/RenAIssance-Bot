from datetime import datetime, timedelta

import aiosqlite


# Функция для удаления связи с резервным аккаунтом, если прошло более 24 часов
async def remove_old_backup_accounts():
    async with aiosqlite.connect('renaissancebot.db') as conn:
        cursor = await conn.cursor()

        # Текущая дата и время
        current_time = datetime.now()

        # Проверяем связи, которым больше 24 часов
        await cursor.execute('''
            SELECT user_id, email
            FROM UserBackupAccounts
            WHERE link_date <= ?
        ''', (current_time - timedelta(days=1),))

        # Получаем все записи, у которых истек срок действия
        rows = await cursor.fetchall()

        for row in rows:
            user_id, email = row

            # Удаляем связь, если прошло более 24 часов
            await cursor.execute('''
                DELETE FROM UserBackupAccounts
                WHERE user_id = ? AND email = ?
            ''', (user_id, email))

        # Применяем изменения
        await conn.commit()
