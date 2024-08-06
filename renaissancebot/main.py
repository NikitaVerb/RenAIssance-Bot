import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from renaissancebot.config_reader import config
from renaissancebot.db import create_db, create_triggers
from renaissancebot.handlers.auth_user import auth_user_start, update_email
from renaissancebot.handlers.user import user_start, registration



async def main():
    bot = Bot(token=config.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    logging.basicConfig(level=logging.DEBUG)
    dp = Dispatcher()

    dp.include_router(auth_user_start.router)
    dp.include_router(user_start.router)
    dp.include_router(registration.router)
    dp.include_router(update_email.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(create_db())
    asyncio.run(main())
    asyncio.run(create_triggers())
