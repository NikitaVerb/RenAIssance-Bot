import logging

import aiosqlite


async def unlink_user_from_account(user_id: int, email_account: str) -> None:
    try:
        async with aiosqlite.connect('renaissancebot.db') as db:
            # Явное использование курсора
            async with db.cursor() as cursor:
                await cursor.execute(
                    '''DELETE FROM UserEmails WHERE user_id = ? AND email = ?''',
                    (user_id, email_account)
                )
            # Фиксация изменений
            await db.commit()
    except Exception as e:
        # Обработка возможных ошибок
        logging.exception(e)
