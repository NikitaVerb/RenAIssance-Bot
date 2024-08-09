import logging

from aiogram import Router, types
from aiogram.filters import Command, CommandObject

import renaissancebot.filters.user_rights
from db import check_account_in_db, check_user_email_in_db, unlink_user_from_account, get_user_id, \
    unlink_all_users_from_account

router = Router()
router.message.filter(renaissancebot.filters.user_rights.UserIsAdmin())


@router.message(Command('unlink'))
async def unlink_from_account_handler(message: types.Message, command: CommandObject):
    try:
        # Проверяем, что команда содержит два аргумента (email аккаунта и email пользователя)
        if not command.args or len(command.args.split()) != 2:
            await message.answer("Неправильный формат команды. Используйте: /unlink <account_email> <user_email>", parse_mode=None)
            return

        # Разделяем аргументы на email аккаунта и email пользователя
        account_email, user_email = command.args.split()

        # Получаем user_id по email пользователя
        user_id = await get_user_id(user_email)
        if user_id is None:
            await message.answer("Пользователь с таким email не найден")
            return
        user_id = int(user_id)

        # Проверяем, что аккаунт существует в базе данных
        if not await check_account_in_db(account_email):
            await message.answer("Такого аккаунта нет в базе")
            return

        # Проверяем, что пользователь существует в базе данных
        if not await check_user_email_in_db(user_email):
            await message.answer("Такой почты пользователя нет в базе")
            return

        # Отвязываем пользователя от аккаунта
        await unlink_user_from_account(user_id, account_email)

        # Отправляем сообщение о успешном отвязывании
        await message.answer("Пользователь успешно отвязан от аккаунта")

    except Exception as e:
        # Обработка исключений и уведомление пользователя о проблеме
        await message.answer("Произошла ошибка при отвязывании пользователя от аккаунта")
        logging.exception(e)


@router.message(Command('unlink_all'))
async def unlink_all_users_from_account_handler(message: types.Message, command: CommandObject):
    try:
        # Проверяем, что команда содержит один аргумент (email аккаунта)
        if not command.args or len(command.args.split()) != 1:
            await message.answer("Неправильный формат команды. Используйте: /unlink_all <account_email>", parse_mode=None)
            return

        # Получаем email аккаунта
        account_email = command.args.strip()

        # Проверяем, что аккаунт существует в базе данных
        if not await check_account_in_db(account_email):
            await message.answer("Такого аккаунта нет в базе")
            return

        # Отвязываем всех пользователей от аккаунта
        await unlink_all_users_from_account(account_email)

        # Отправляем сообщение о успешном отвязывании всех пользователей
        await message.answer(f"Все пользователи успешно отвязаны от аккаунта {account_email}")

    except Exception as e:
        # Обработка исключений и уведомление пользователя о проблеме
        await message.answer("Произошла ошибка при отвязывании всех пользователей от аккаунта")
        logging.exception(e)