import aiosqlite
import sqlite3
import os


async def backup_database():
    db_path = os.path.abspath('../Data/renaissancebot.db')
    backup_path = os.path.abspath('../Data/backup_renaissancebot.db')

    async with aiosqlite.connect(db_path) as source_db:
        # Открываем файл для бэкапа
        dest_db = sqlite3.connect(backup_path)

        # Используем встроенный метод backup
        await source_db.backup(dest_db)
        dest_db.close()