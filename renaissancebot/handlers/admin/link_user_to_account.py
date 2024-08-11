import logging

from aiogram import Router, types
from aiogram.filters import Command, CommandObject

import renaissancebot.filters.user_rights
from db import check_account_in_db, check_user_email_in_db, get_user_id, \
    add_link_user_to_account, check_link_exists

router = Router()
router.message.filter(renaissancebot.filters.user_rights.UserIsAdmin())


@router.message(Command('link'))
async def link_user_to_account_handler(message: types.Message, command: CommandObject):
    try:
        # Проверяем, что команда содержит два аргумента (email аккаунта и email пользователя)
        if not command.args or len(command.args.split()) != 2:
            await message.answer("Неправильный формат команды. Используйте: /link <account_email> <user_email>",
                                 parse_mode=None)
            return

        # Разделяем аргументы на email аккаунта и email пользователя
        account_email, user_email = command.args.split()

        if not await check_account_in_db(account_email):
            await message.answer("Такого аккаунта нет в базе")
            return

        # Получаем user_id по email пользователя
        user_id = await get_user_id(user_email)
        if user_id is None:
            await message.answer("Пользователь с таким email не найден")
            return
        user_id = int(user_id)

        # Проверяем, что аккаунт существует в базе данных

        if await check_link_exists(user_id, account_email):
            await message.answer("Такая связь уже существует")
            return

        # Проверяем, что пользователь существует в базе данных
        if not await check_user_email_in_db(user_email):
            await message.answer("Пользователь с таким email не найден")
            return

        # Отвязываем пользователя от аккаунта
        await add_link_user_to_account(user_id, account_email)

        # Отправляем сообщение о успешном отвязывании
        await message.answer("Пользователь успешно привязан к аккаунту")

    except Exception as e:
        # Обработка исключений и уведомление пользователя о проблеме
        await message.answer("Произошла ошибка при привязывании пользователя от аккаунта")
        logging.exception(e)
