from aiogram import Bot

from db import get_all_admin_ids


# Функция для отправки сообщения всем администраторам
async def send_message_to_all_admins(bot: Bot, message_text: str):
    # Получаем список ID всех администраторов
    admin_ids = await get_all_admin_ids()

    # Отправляем сообщение каждому администратору
    for admin_id in admin_ids:
        await bot.send_message(chat_id=admin_id, text=message_text)
