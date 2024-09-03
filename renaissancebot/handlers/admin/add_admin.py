from aiogram import Router
from aiogram import types
from aiogram.filters import Command

from db import add_admin_to_db, check_user_is_admin

router = Router()


@router.message(Command('add_admin'))
async def add_admin_handler(message: types.Message):
    # Разделяем сообщение на команду и admin_id
    args = message.text.split()

    if len(args) != 2:
        await message.answer("Использование команды: /add_admin <admin_id>", parse_mode=None)
        return

    try:
        admin_id = int(args[1])
    except ValueError:
        await message.answer("admin_id должен быть числом.")
        return

    # Проверяем, является ли пользователь, вызывающий команду, администратором (если требуется)
    if not await check_user_is_admin(message.from_user.id):
        await message.answer("У вас нет прав на добавление админов.")
        return

    # Проверяем, является ли указанный пользователь уже администратором
    if await check_user_is_admin(admin_id):
        await message.answer(f"Пользователь с ID {admin_id} уже является админом.")
    else:
        # Если не является, то добавляем его в таблицу админов
        await add_admin_to_db(admin_id)
        await message.answer(f"Пользователь с ID {admin_id} успешно добавлен в админы.")