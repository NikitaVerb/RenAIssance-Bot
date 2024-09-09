import logging

import aiosqlite


async def unlink_all_users_from_account(email_account: str) -> None:
    try:
        async with aiosqlite.connect('../Data/renaissancebot.db') as db:
            async with db.cursor() as cursor:
                await cursor.execute(
                    '''DELETE FROM UserEmails WHERE email = ?''',
                    (email_account,)
                )
            await db.commit()
    except Exception as e:
        # Обработка возможных ошибок и логирование
        logging.exception(e)
