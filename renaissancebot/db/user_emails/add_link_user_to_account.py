import aiosqlite


async def add_link_user_to_account(user_id: int, email_account: str) -> None:
    async with aiosqlite.connect('renaissancebot.db') as db:
        await db.execute('''
            INSERT INTO UserEmails (user_id, email) 
            VALUES (?, ?)
        ''', (user_id, email_account))
        await db.commit()

    