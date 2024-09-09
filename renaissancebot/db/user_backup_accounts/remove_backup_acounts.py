from datetime import datetime, timedelta
import aiosqlite


# Функция для удаления связи с резервным аккаунтом, если прошло более 24 часов
async def remove_old_backup_accounts():
    async with aiosqlite.connect('renaissancebot.db') as conn:
        cursor = await conn.cursor()

        # Текущая дата и время
        current_time = datetime.now()
        cutoff_time = current_time - timedelta(days=1)

        # Проверяем связи, которым больше 24 часов
        await cursor.execute('''
            SELECT user_id, email, link_date
            FROM UserBackupAccounts
            WHERE link_date <= ?
        ''', (cutoff_time,))

        # Получаем все записи, у которых истек срок действия
        rows = await cursor.fetchall()

        if rows:
            for row in rows:
                user_id, email, link_date = row

                # Выводим данные, которые собираемся удалить для отладки
                print(f"Deleting user_id: {user_id}, email: {email}, link_date: {link_date}")

                # Удаляем связь, если прошло более 24 часов
                await cursor.execute('''
                    DELETE FROM UserBackupAccounts
                    WHERE user_id = ? AND email = ?
                ''', (user_id, email))
        else:
            print("No rows to delete.")

        # Применяем изменения
        await conn.commit()
