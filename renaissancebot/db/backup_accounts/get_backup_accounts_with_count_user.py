# выводить список аккаунтов и количество привязанных к этим аккаунтам пользователей

import aiosqlite


async def get_backup_accounts_with_user_count():
    async with aiosqlite.connect('renaissancebot.db') as db:
        async with db.execute('''
            SELECT BackupAccounts.email, BackupAccounts.password, COUNT(UserBackupAccounts.user_id) AS user_count
            FROM BackupAccounts
            LEFT JOIN UserBackupAccounts ON BackupAccounts.email = UserBackupAccounts.email
            GROUP BY BackupAccounts.email
            ORDER BY user_count DESC, BackupAccounts.email ASC
        ''') as cursor:
            result = await cursor.fetchall()
            return result
