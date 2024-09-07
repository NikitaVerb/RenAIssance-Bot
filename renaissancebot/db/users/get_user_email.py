import aiosqlite


async def get_user_email(user_id: int) -> str:
    async with aiosqlite.connect('renaissancebot.db') as db:
        async with db.execute('''SELECT email FROM Users WHERE user_id = ?''', (user_id,)) as cursor:
            row = await cursor.fetchone()
            if row is not None:
                return row[0]  # Возвращаем первый элемент из кортежа, который содержит email
