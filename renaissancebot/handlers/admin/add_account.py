import logging

from aiogram import Router
from aiogram import types
from aiogram.filters import Command, CommandObject
from db import add_account_to_db, check_account_in_db

import renaissancebot.filters.user_rights

router = Router()
router.message.filter(renaissancebot.filters.user_rights.UserIsAdmin())


@router.message(Command('add_account'))
async def add_account(message: types.Message, command: CommandObject):
    try:
        # Проверяем, что команда содержит два аргумента (email и пароль)
        if not command.args or len(command.args.split()) != 2:

            await message.answer("Неправильный формат команды. Используйте: /add_account <email> <password>")
            return


        # Разделяем аргументы на email и пароль
        email, password = command.args.split()

        if await check_account_in_db(email):
            await message.answer("Такой аккаунт уже имеется в базе")
            return
        # Добавляем учетную запись в базу данных
        await add_account_to_db(email, password)

        # Отправляем сообщение о успешном добавлении
        await message.answer("Аккаунт успешно добавлен")

    except Exception as e:
        # Обработка исключений и уведомление пользователя о проблеме
        await message.answer(f"Произошла ошибка при добавлении аккаунта")
        logging.exception(e)