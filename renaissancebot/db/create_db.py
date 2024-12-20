import aiosqlite


async def create_db():
    async with aiosqlite.connect('../Data/renaissancebot.db') as conn:
        cursor = await conn.cursor()

        # Создаем таблицу пользователей
        await cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                user_id INTEGER PRIMARY KEY,
                email TEXT NOT NULL,
                purchase_date DATE DEFAULT NULL,
                expiration_date DATE DEFAULT NULL,
                spent INTEGER DEFAULT 0 NOT NULL,
                used_backup_account DATETIME DEFAULT NULL,
                notified INTEGER,
                CHECK (purchase_date IS NULL OR expiration_date IS NULL OR purchase_date <= expiration_date)
            )
        ''')

        # Создаем таблицу почт
        await cursor.execute('''
            CREATE TABLE IF NOT EXISTS Emails (
                email TEXT PRIMARY KEY,
                password TEXT NOT NULL
            )
        ''')

        # Создаем таблицу связей пользователей и почт
        await cursor.execute('''
            CREATE TABLE IF NOT EXISTS UserEmails (
                user_id INTEGER NOT NULL UNIQUE,
                email TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES Users (user_id) ON DELETE RESTRICT,
                FOREIGN KEY (email) REFERENCES Emails (email) ON DELETE RESTRICT,
                PRIMARY KEY (user_id, email)
            )
        ''')

        await cursor.execute('''CREATE TABLE IF NOT EXISTS Admins(
                                        user_id INTEGER PRIMARY KEY)''')

        # Создаем таблицу резервных аккаунтов
        await cursor.execute('''
                    CREATE TABLE IF NOT EXISTS BackupAccounts (
                        email TEXT PRIMARY KEY,
                        password TEXT NOT NULL
                    )
                ''')

        await cursor.execute('''
                    CREATE TABLE IF NOT EXISTS UserBackupAccounts (
                        user_id INTEGER NOT NULL UNIQUE,
                        email TEXT NOT NULL,
                        link_date DATETIME DEFAULT NULL,
                        FOREIGN KEY (user_id) REFERENCES Users (user_id) ON DELETE RESTRICT,
                        FOREIGN KEY (email) REFERENCES BackupAccounts (email) ON DELETE RESTRICT,
                        PRIMARY KEY (user_id, email)
                    )
                ''')

        await conn.commit()
