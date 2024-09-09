import aiosqlite


async def add_account_to_db(email: str, password: str):
    async with aiosqlite.connect('../Data/renaissancebot.db') as conn:
        cursor = await conn.cursor()
        await cursor.execute('''INSERT INTO Emails (email, password) VALUES (?, ?)''', (email, password))
        await conn.commit()
