# выводить список аккаунтов и количество привязанных к этим аккаунтам пользователей

import aiosqlite


async def get_emails_with_user_count():
    async with aiosqlite.connect('../Data/renaissancebot.db') as db:
        async with db.execute('''
            SELECT Emails.email, Emails.password, COUNT(UserEmails.user_id) AS user_count
            FROM Emails
            LEFT JOIN UserEmails ON Emails.email = UserEmails.email
            GROUP BY Emails.email
            ORDER BY user_count DESC, Emails.email ASC
        ''') as cursor:
            result = await cursor.fetchall()
            return result
