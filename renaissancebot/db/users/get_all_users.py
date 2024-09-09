import aiosqlite


async def get_all_users():
    async with aiosqlite.connect('../Data/renaissancebot.db') as db:
        async with db.execute('''SELECT * FROM Users''') as cursor:
            row = await cursor.fetchall()
            return row
