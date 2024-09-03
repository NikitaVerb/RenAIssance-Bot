from aiogram import Router
from aiogram import types
from aiogram.filters import Command, CommandObject

import renaissancebot.filters.user_rights
from db import update_account_password

router = Router()
router.message.filter(renaissancebot.filters.user_rights.UserIsAdmin())


@router.message(Command('update_password'))
async def update_password(message: types.Message, command: CommandObject):
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
