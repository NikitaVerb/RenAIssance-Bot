import aiosqlite


async def create_triggers():
    async with aiosqlite.connect('renaissancebot.db') as conn:
        cursor = await conn.cursor()

        # Триггер для увеличения user_count при добавлении записи в UserEmails
        await cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS increase_user_count
            AFTER INSERT ON UserEmails
            FOR EACH ROW
            BEGIN
                UPDATE Emails SET user_count = user_count + 1 WHERE email = NEW.email;
            END;
        ''')

        # Триггер для уменьшения user_count при удалении записи из UserEmails
        await cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS decrease_user_count
            AFTER DELETE ON UserEmails
            FOR EACH ROW
            BEGIN
                UPDATE Emails SET user_count = user_count - 1 WHERE email = OLD.email;
            END;
        ''')

        await conn.commit()

# Запуск функции для создания триггеров
