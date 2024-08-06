import aiosqlite


async def create_db():
    async with aiosqlite.connect('renaissancebot.db') as conn:
        cursor = await conn.cursor()

        # Создаем таблицу пользователей
        await cursor.execute('''CREATE TABLE IF NOT EXISTS Users(
                                user_id INTEGER PRIMARY KEY,
                                email TEXT NOT NULL)''')

        # Создаем таблицу почт
        await cursor.execute('''CREATE TABLE IF NOT EXISTS Emails(
                                email TEXT PRIMARY KEY,
                                password TEXT NOT NULL,
                                user_count INTEGER DEFAULT 0)''')

        # Создаем таблицу связей пользователей и почт
        await cursor.execute('''CREATE TABLE IF NOT EXISTS UserEmails(
                                user_id INTEGER,
                                email TEXT,
                                FOREIGN KEY (user_id) REFERENCES Users (user_id),
                                FOREIGN KEY (email) REFERENCES Emails (email),
                                PRIMARY KEY (user_id, email))''')

        await conn.commit()
