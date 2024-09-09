import logging

from aiogram import Bot
from aiogram.enums import ParseMode

from db import notify_expired_users
from keyboards import back_to_menu_inline_kb


async def send_expiry_notifications(bot: Bot):
    # Получаем список пользователей с истекшей подпиской
    expired_users = await notify_expired_users()

    if expired_users:
        for user in expired_users:
            user_id = user[0]

            # Отправляем сообщение о завершении подписки
            try:
                await bot.send_message(
                    chat_id=user_id,
                    text="Ваша подписка истекла."
                         " Пожалуйста, продлите свою подписку, чтобы продолжать пользоваться нашими услугами.",
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=back_to_menu_inline_kb()
                )
                logging.info(f"Notification sent to user_id: {user_id}")
            except Exception as e:
                logging.error(f"Failed to send message to user {user_id}: {e}")
    else:
        logging.info("No expired users to notify.")
