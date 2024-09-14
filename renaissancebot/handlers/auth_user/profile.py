from datetime import datetime, timedelta

from aiogram import Router, types, F, Bot
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from db import get_user_email, get_user_account, get_user_expiration_date, get_account_password, \
    get_used_backup_account_date, get_user_backup_account, get_backup_account_password, check_user_in_db, \
    check_user_backup_account
from keyboards import reg_inline_markup, backup_account_inline_kb, requests_have_ended_inline_kb

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
    backup_account_inf: str = ''
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
            if await check_user_backup_account(user_id):
                email_backup_account = await get_user_backup_account(user_id)
                backup_account_password = await get_backup_account_password(email_backup_account)
                backup_account_inf = (f"\n**Логин резервного аккаунта:** `{email_backup_account or ''}`\n\n"
                                      f"**Пароль от резервного аккаунта:** `{backup_account_password or ''}`")
    else:
        date_expiration = 'Вы ещё не оформляли подписку'

    # Формируем ответ
    cart = f"**Ваш email:** {email}\n\n"
    cart += f"**Логин ChatGPT:** {text_account_email}\n\n"  # Логин всегда показывается

    # Добавляем пароль, если он есть
    if password:
        cart += f"**Пароль от аккаунта:** `{password}` (нажмите, чтобы скопировать)\n\n"
    else:
        cart += "**Пароль от аккаунта:** нет действительного пароля от аккаунта ChatGPT\n\n"

    # Дата окончания подписки
    cart += f"**Дата окончания подписки:** {date_expiration}\n"
    cart += backup_account_inf
    # Отправляем сообщение
    await bot.edit_message_text(chat_id=message.chat.id,
                                message_id=message.message_id, text=cart,
                                reply_markup=requests_have_ended_inline_kb(),
                                parse_mode=ParseMode.MARKDOWN)


@router.callback_query(F.data == "req_have_ended")
async def req_have_ended(callback: CallbackQuery, bot: Bot):
    # Получаем дату последнего запроса к резервному аккаунту
    backup_account_button = True
    user_id = callback.from_user.id

    date_expiration = await get_user_expiration_date(user_id)

    if not date_expiration or datetime.strptime(date_expiration.strip(), '%Y-%m-%d').date() < datetime.now().date():
        backup_account_button = False

    used_backup_account_date = await get_used_backup_account_date(user_id)

    if used_backup_account_date:
        used_backup_account_date = datetime.strptime(used_backup_account_date.strip(), '%Y-%m-%d %H:%M:%S')
        if used_backup_account_date + timedelta(days=3) > datetime.now():
            backup_account_button = False

    if backup_account_button:
        text = ("Если у Вас исчерпан лимит запросов, то вы можете получить временный резервный аккаунт, "
                "данные от него будут отображаться у вас в профиле в течении одного дня.\n"
                "После нажатия кнопка будет отсутствовать следующие 3 дня")
    else:
        text = ("Вы уже запрашивали резервный аккаунт,"
                " кнопка появится по истечении  3-х дней после её последнего нажатия")

    await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                text=text, reply_markup=backup_account_inline_kb(backup_account_button))
