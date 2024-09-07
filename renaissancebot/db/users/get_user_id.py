import aiosqlite


async def get_user_id(user_email: str) -> str:
    async with aiosqlite.connect('renaissancebot.db') as db:
        async with db.execute('''SELECT user_id FROM Users WHERE email = ?''', (user_email,)) as cursor:
            row = await cursor.fetchone()
            if row is not None:
                return row[0]  # Возвращаем первый элемент из кортежа, который содержит user_id
