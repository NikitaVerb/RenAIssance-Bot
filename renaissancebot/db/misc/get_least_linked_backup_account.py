import aiosqlite


async def get_least_linked_backup_account() -> str:
    async with aiosqlite.connect('../Data/renaissancebot.db') as db:
        async with db.execute('''
            SELECT BackupAccounts.email
            FROM BackupAccounts
            LEFT JOIN UserBackupAccounts ON BackupAccounts.email = UserBackupAccounts.email
            WHERE BackupAccounts.email NOT LIKE '%_ind'
            GROUP BY BackupAccounts.email
            HAVING COUNT(UserBackupAccounts.user_id) < 10
            ORDER BY COUNT(UserBackupAccounts.user_id) ASC, BackupAccounts.email ASC
            LIMIT 1
        ''') as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None
