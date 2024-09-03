import aiosqlite


async def update_account_password(email: str, new_password: str) -> None:
    async with aiosqlite.connect('renaissancebot.db') as db:
        # Обновляем пароль для указанного email
        await db.execute('''
            UPDATE Emails
            SET password = ?
            WHERE email = ?
        ''', (new_password, email))

        # Подтверждаем изменения
        await db.commit()
