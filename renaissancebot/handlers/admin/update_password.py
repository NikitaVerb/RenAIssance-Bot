import asyncio

from aiogram import Router, Bot
from aiogram import types
from aiogram.filters import Command, CommandObject

import renaissancebot.filters.user_rights
from db import update_account_password, get_current_users_on_account
from keyboards import back_to_menu_inline_kb

router = Router()
router.message.filter(renaissancebot.filters.user_rights.UserIsAdmin())


async def send_password_change_message(user_id: int, bot: Bot):
    await bot.send_message(chat_id=user_id,
                           text='Пароль от вашего аккаунта был изменен, новый пароль отобразится в вашем профиле',
                           reply_markup=back_to_menu_inline_kb())


@router.message(Command('update_password'))
async def update_password(message: types.Message, command: CommandObject, bot: Bot):
    args = command.args.split()

    # Проверяем, что указаны оба аргумента: email и новый пароль
    if len(args) != 2:
        await message.answer(
            "Неправильный формат команды.\nИспользуйте: /update_password <account_email> <new_password>")
        return

    account_email, new_password = args

    # Обновляем пароль в базе данных
    await update_account_password(account_email, new_password)
    await message.answer(f"Пароль для {account_email} успешно обновлен.")

    users = await get_current_users_on_account(account_email)

    # Отправляем уведомление всем пользователям параллельно
    if users:
        await asyncio.gather(*[send_password_change_message(int(user_id[0]), bot) for user_id in users])
    else:
        await message.answer("Нет пользователей, привязанных к этому аккаунту.")
