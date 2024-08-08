import logging

from aiogram import Router
from aiogram import types
from aiogram.filters import Command
from email_validator import EmailNotValidError, validate_email

from db import update_user_email, check_user_email_in_db

router = Router()


@router.message(Command('update_email'))
async def update_email_command(message: types.Message):
    # Проверяем, что команда содержит аргумент
    if len(message.text.split()) != 2:
        await message.reply("Используйте команду в формате: /update_email <new_email>")
        return

        # Извлекаем новый email из команды
    _, new_email = message.text.split()

    try:
        # Проверяем валидность email
        valid = validate_email(new_email)
        email = valid.email

        if await check_user_email_in_db(email):
            await message.reply("Пользователь с таким email уже существует")
        else:
            await update_user_email(message.from_user.id, email)
            await message.reply(f"Ваша почта была обновлена на {new_email}.", parse_mode=None)
    except EmailNotValidError as e:
        await message.reply(f"Неверный формат email. Пожалуйста, введите корректный email. Ошибка: {str(e)}",
                            parse_mode=None)
    except Exception as e:
        logging.error(f"Ошибка при обновлении почты: {e}")
        await message.reply("Произошла ошибка при обновлении вашей почты.", parse_mode=None)
