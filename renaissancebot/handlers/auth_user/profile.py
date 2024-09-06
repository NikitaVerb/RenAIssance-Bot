from datetime import datetime

from aiogram import Router, types, F, Bot
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from db import get_user_email, get_user_account, get_user_expiration_date, get_account_password, check_user_in_db
from keyboards import back_to_menu_inline_kb, reg_inline_markup

router = Router()


# Обработчик callback'а
@router.callback_query(F.data.startswith('profile'))
async def profile(callback: CallbackQuery, bot: Bot):
    if not (await check_user_in_db(callback.from_user.id)):
        await bot.edit_message_text(chat_id=callback.message.chat.id,
                                    message_id=callback.message.message_id, text=
                                    f'Если хотите приобрести подписку или отслеживать статус уже купленной подписки,'
                                    f' то вам нужно зарегистрироваться'
                                    , reply_markup=reg_inline_markup())
        return
    await profile_handler(callback.message, callback.from_user.id, bot)


# Основная функция для обработки профиля
async def profile_handler(message: types.Message, user_id: int, bot: Bot):
    # Получаем данные пользователя
    email = await get_user_email(user_id)
    account_email = await get_user_account(user_id)
    if account_email:
        # Убираем "_ind" из названия аккаунта, если это индивидуальный аккаунт
        if account_email.endswith('_ind'):
            account_email = account_email[:-4]
        text_account_email = f'`{account_email}` (нажмите, чтобы скопировать)'
    else:
        text_account_email = 'у вас нет аккаунта ChatGPT'
    date_expiration = await get_user_expiration_date(user_id)

    # Проверяем дату окончания подписки
    password = None  # Инициализируем пароль по умолчанию
    if date_expiration:
        expiration_date = datetime.strptime(date_expiration.strip(), '%Y-%m-%d').date()
        if expiration_date > datetime.now().date():
            # Подписка действительна, получаем пароль
            password = await get_account_password(account_email)
    else:
        date_expiration = 'Вы ещё не оформляли подписку'

    # Формируем ответ
    cart = f"Ваш email: {email}\n\n"
    cart += f"Логин ChatGPT: {text_account_email}\n\n"  # Логин всегда показывается

    # Добавляем пароль, если он есть
    if password:
        cart += f"Пароль от аккаунта: `{password}` (нажмите, чтобы скопировать)\n\n"
    else:
        cart += "Пароль от аккаунта: нет действительного пароля от аккаунта ChatGPT\n\n"

    # Дата окончания подписки
    cart += f"Дата окончания подписки: {date_expiration}\n\n"

    # Отправляем сообщение
    await bot.edit_message_text(chat_id=message.chat.id,
                                message_id=message.message_id, text=cart, reply_markup=back_to_menu_inline_kb(),
                                parse_mode=ParseMode.MARKDOWN)
