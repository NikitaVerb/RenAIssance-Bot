import logging

from aiogram import Router
from aiogram import types
from aiogram.filters import Command, CommandObject

import renaissancebot.filters.user_rights
from db import add_account_to_db, add_backup_account_or_update_password, check_account_in_db

router = Router()
router.message.filter(renaissancebot.filters.user_rights.UserIsAdmin())


@router.message(Command('add_account'))
async def add_account(message: types.Message, command: CommandObject):
    try:
        # Проверяем, что команда содержит два или три аргумента (email, password, [r])
        args = command.args.split()

        if len(args) < 2 or len(args) > 3:
            await message.answer(
                "Неправильный формат команды. Используйте: /add_account <email> <password> [r]",
                parse_mode=None
            )
            return

        # Разделяем аргументы на email и пароль
        email = args[0]
        password = args[1]
        is_backup = len(args) == 3 and args[2] == 'r'

        if await check_account_in_db(email):
            await message.answer("Такой аккаунт уже имеется в базе")
            return

        # Добавляем резервный или обычный аккаунт
        if is_backup:
            await add_backup_account_or_update_password(email, password)
            await message.answer("Резервный аккаунт успешно добавлен")
        else:
            await add_account_to_db(email, password)
            await message.answer("Аккаунт успешно добавлен")

    except Exception as e:
        # Обработка исключений и уведомление пользователя о проблеме
        await message.answer(f"Произошла ошибка при добавлении аккаунта")
        logging.exception(e)
