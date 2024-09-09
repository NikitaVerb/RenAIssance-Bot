from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from db import remove_old_backup_accounts
from handlers.admin.send_expire_notification import send_expiry_notifications


# Настройка планировщика для периодического запуска задачи
def setup_scheduler(bot: Bot):
    scheduler = AsyncIOScheduler()

    # Добавляем задачу, которая будет запускаться каждые 24 часа
    scheduler.add_job(remove_old_backup_accounts, 'interval', hours=1)
    scheduler.add_job(send_expiry_notifications, 'interval', hours=1, args=[bot])

    # Запускаем планировщик
    scheduler.start()
