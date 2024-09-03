from datetime import datetime

from aiogram import Router, types
from aiogram.filters import Command

from db import get_user_email, get_user_account, get_user_expiration_date, get_account_password

router = Router()


@router.message(Command('profile'))
async def profile_handler(message: types.Message):
    user_id = message.from_user.id

    # Получаем данные пользователя
    email = await get_user_email(user_id)
    account_email = await get_user_account(user_id) or 'у вас нет аккаунта ChatGPT'
    date_expiration = await get_user_expiration_date(user_id)

    # Проверяем дату окончания подписки
    if date_expiration:
        expiration_date = datetime.strptime(date_expiration.strip(), '%Y-%m-%d').date()
        if expiration_date > datetime.now().date():
            password = await get_account_password(account_email)
        else:
            password = 'нет действительного пароля от аккаунта ChatGPT'
    else:
        password = 'нет действительного пароля от аккаунта ChatGPT'
        date_expiration = '-----------------'

    if account_email.endswith('_ind'):
        account_email = account_email[:-4]
    # Формируем и отправляем ответ
    cart = (f"Ваш email: {email}\n\n"
            f"Аккаунт ChatGPT: {account_email}\n\n"
            f"Пароль от аккаунта: {password}\n\n"
            f"Дата окончания подписки: {date_expiration}\n\n")

    await message.answer(cart)
