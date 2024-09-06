from apscheduler.schedulers.asyncio import AsyncIOScheduler

from db import remove_old_backup_accounts


# Настройка планировщика для периодического запуска задачи
def setup_scheduler():
    scheduler = AsyncIOScheduler()

    # Добавляем задачу, которая будет запускаться каждые 24 часа
    scheduler.add_job(remove_old_backup_accounts, 'interval', hours=1)

    # Запускаем планировщик
    scheduler.start()
