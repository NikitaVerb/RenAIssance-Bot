from aiogram import Router
from aiogram import types
from aiogram.filters import Command

from db import add_to_users_spent, check_user_email_in_db, get_user_id

router = Router()


@router.message(Command('add_spend'))
async def add_spend_handler(message: types.Message):
    args = message.text.split()

    # Проверяем, что переданы два аргумента: email и сумма
    if len(args) != 3:
        await message.answer("Используйте команду в формате: /add_spend <user_email> <amount>")
        return

    user_email = args[1]
    try:
        amount = int(args[2])  # Пробуем конвертировать сумму в число
    except ValueError:
        await message.answer("Сумма должна быть числом. Пример: /add_spend user@example.com 100")
        return

    # Проверяем, существует ли пользователь в базе данных
    user_exists = await check_user_email_in_db(user_email)
    if not user_exists:
        await message.answer(f"Пользователь с email {user_email} не найден.")
        return

    # Обновляем потраченные средства пользователя
    user_id = int(await get_user_id(user_email))
    await add_to_users_spent(user_id, amount)

    await message.answer(f"Пользователю {user_email} добавлено {amount} к потраченным средствам.")
