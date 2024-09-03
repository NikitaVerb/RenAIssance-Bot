import aiosqlite


async def get_most_linked_email_account() -> str:
    async with aiosqlite.connect('renaissancebot.db') as db:
        async with db.execute('''
            SELECT Emails.email
            FROM Emails
            LEFT JOIN UserEmails ON Emails.email = UserEmails.email
            GROUP BY Emails.email
            HAVING COUNT(UserEmails.user_id) < 10
            ORDER BY COUNT(UserEmails.user_id) DESC, Emails.email ASC
            LIMIT 1
        ''') as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None
