import logging

import aiosqlite


async def unlink_user_from_backup_account(user_id: int) -> None:
    try:
        async with aiosqlite.connect('renaissancebot.db') as db:
            # Явное использование курсора
            async with db.cursor() as cursor:
                await cursor.execute(
                    '''DELETE FROM UserBackupAccounts WHERE user_id = ?''',
                    (user_id,)
                )
            # Фиксация изменений
            await db.commit()
    except Exception as e:
        # Обработка возможных ошибок
        logging.exception(e)
