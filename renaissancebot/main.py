import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from filters.setup_scheduler import setup_scheduler
from renaissancebot.config_reader import config
from renaissancebot.db import create_db
from renaissancebot.handlers.admin import add_account, unlink_from_account, link_user_to_account, get_accounts, \
    get_data, admin_helper, update_password, delete_account, add_admin, add_spent
from renaissancebot.handlers.auth_user import auth_user_start, update_email, profile, pay, backup_account
from renaissancebot.handlers.user import user_start, registration, utils, catalog, menu, faq


async def main():

    bot = Bot(token=config.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    setup_scheduler(bot)
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    dp = Dispatcher()
    dp.include_router(admin_helper.router)
    dp.include_router(auth_user_start.router)
    dp.include_router(user_start.router)
    dp.include_router(registration.router)
    dp.include_router(update_email.router)
    dp.include_router(utils.router)
    dp.include_router(catalog.router)
    dp.include_router(add_account.router)
    dp.include_router(unlink_from_account.router)
    dp.include_router(link_user_to_account.router)
    dp.include_router(get_accounts.router)
    dp.include_router(get_data.router)
    dp.include_router(profile.router)
    dp.include_router(pay.router)
    dp.include_router(update_password.router)
    dp.include_router(delete_account.router)
    dp.include_router(add_admin.router)
    dp.include_router(menu.router)
    dp.include_router(faq.router)
    dp.include_router(backup_account.router)
    dp.include_router(add_spent.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=False)


if __name__ == "__main__":
    asyncio.run(create_db())
    asyncio.run(main())
