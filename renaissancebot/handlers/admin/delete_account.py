from aiogram import Router
from aiogram import types
from aiogram.filters import Command

from db import check_account_links, delete_account_from_db

router = Router()


@router.message(Command('delete_account'))
async def delete_account_handler(message: types.Message):
    # Разделяем сообщение на команду и email
    args = message.text.split()

    if len(args) != 2:
        await message.answer("Использование команды: /delete_account <account_email>", parse_mode=None)
        return

    account_email = args[1]

    # Проверяем наличие связей с этим email в таблице UserEmails
    if await check_account_links(account_email):
        await message.answer(f"Email {account_email} связан с пользователями и не может быть удален.")
    else:
        # Если связей нет, удаляем email из таблицы Emails
        if await delete_account_from_db(account_email):
            await message.answer(f"Email {account_email} успешно удален.")
        else:
            await message.answer(f"Не удалось удалить {account_email}.")
