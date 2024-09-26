import aiosqlite


async def reset_used_backup_account(user_id):
    async with aiosqlite.connect('../Data/renaissancebot.db') as conn:
        cursor = await conn.cursor()

        # Обновляем поле used_backup_account на NULL для указанного пользователя
        await cursor.execute('''
            UPDATE Users
            SET used_backup_account = NULL
            WHERE user_id = ?
        ''', (user_id,))

        # Подтверждаем изменения
        await conn.commit()