from datetime import datetime

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery

from db import get_user_email, get_user_account, get_user_expiration_date, get_account_password, check_user_in_db
from keyboards import back_to_menu_inline_kb, reg_inline_markup


router = Router()


# Обработчик callback'а
@router.callback_query(F.data.startswith('profile'))
async def profile(callback: CallbackQuery):
    await callback.answer()
    if not (await check_user_in_db(callback.from_user.id)):
        await callback.message.answer(
            f'Если хотите приобрести подписку или отслеживать статус уже купленной подписки,'
            f' то вам нужно зарегестрироваться'
            , reply_markup=reg_inline_markup())
        return
    await profile_handler(callback.message, callback.from_user.id)


# Обработчик команды /profile
@router.message(Command('profile'))
async def profile_command(message: types.Message):
    if not (await check_user_in_db(message.from_user.id)):
        await message.answer(
            f'Если хотите приобрести подписку или отслеживать статус уже купленной подписки,'
            f' то вам нужно зарегестрироваться'
            , reply_markup=reg_inline_markup())
        return
    await profile_handler(message, message.from_user.id)


# Основная функция для обработки профиля
async def profile_handler(message: types.Message, user_id: int):
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

    # Убираем "_ind" из названия аккаунта, если это индивидуальный аккаунт
    if account_email.endswith('_ind'):
        account_email = account_email[:-4]

    # Формируем и отправляем ответ
    cart = (f"Ваш email: {email}\n\n"
            f"Аккаунт ChatGPT: {account_email}\n\n"
            f"Пароль от аккаунта: {password}\n\n"
            f"Дата окончания подписки: {date_expiration}\n\n")

    await message.answer(cart, reply_markup=back_to_menu_inline_kb())
