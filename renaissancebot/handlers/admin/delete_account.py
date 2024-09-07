from aiogram import Router
from aiogram import types
from aiogram.filters import Command

from db import check_account_links, delete_account_from_db, delete_backup_account_from_db, is_backup_account, \
    check_backup_account_links

router = Router()


@router.message(Command('delete_account'))
async def delete_account_handler(message: types.Message):
    # Разделяем сообщение на команду и email
    args = message.text.split()

    if len(args) != 2:
        await message.answer("Использование команды: /delete_account <account_email>", parse_mode=None)
        return

    account_email = args[1]

    # Проверяем, является ли аккаунт резервным
    if await is_backup_account(account_email):
        # проверяем наличие связей с этим резервным аккаунтом в таблице UserBackupAccounts
        if await check_backup_account_links(account_email):
            await message.answer(f"Резервный аккаунт {account_email} связан с пользователями и не может быть удален.")
        else:
            # Удаление резервного аккаунта
            if await delete_backup_account_from_db(account_email):
                await message.answer(f"Резервный аккаунт {account_email} успешно удален.")
            else:
                await message.answer(f"Не удалось удалить резервный аккаунт {account_email}.")
    else:
        # Проверяем наличие связей с этим email в основной таблице UserEmails
        if await check_account_links(account_email):
            await message.answer(f"Аккаунт {account_email} связан с пользователями и не может быть удален.")
        else:
            # Если связей нет, удаляем основной аккаунт
            if await delete_account_from_db(account_email):
                await message.answer(f"Email {account_email} успешно удален.")
            else:
                await message.answer(f"Не удалось удалить {account_email}.")
