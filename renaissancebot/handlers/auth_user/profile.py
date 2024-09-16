from datetime import datetime, timedelta

from aiogram import Router, types, F, Bot
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from db import get_user_account, get_user_expiration_date, get_account_password, \
    get_used_backup_account_date, get_user_backup_account, get_backup_account_password, check_user_in_db, \
    check_user_backup_account
from keyboards import backup_account_inline_kb, requests_have_ended_inline_kb, \
    reg_from_profile_inline_markup, back_to_menu_inline_kb

router = Router()


# Обработчик callback'а для команды профиля
@router.callback_query(F.data.startswith('profile'))
async def profile(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id

    # Проверка, зарегистрирован ли пользователь
    if not await check_user_in_db(user_id):
        await bot.edit_message_text(chat_id=callback.message.chat.id,
                                    message_id=callback.message.message_id,
                                    text='Для покупки подписки или отслеживания её статуса необходимо зарегистрироваться.',
                                    reply_markup=reg_from_profile_inline_markup())
        return

    # Обрабатываем профиль пользователя
    await profile_handler(callback.message, user_id, bot)


# Основная функция для отображения профиля
async def profile_handler(message: types.Message, user_id: int, bot: Bot):
    # Получаем основные данные пользователя
    account_email = await get_user_account(user_id)
    date_expiration = await get_user_expiration_date(user_id)
    backup_account_inf = ''
    account_is_ind = True if account_email.endswith('_ind') else False
    # Проверяем срок действия подписки
    if date_expiration:
        expiration_date = datetime.strptime(date_expiration.strip(), '%Y-%m-%d').date()
        # Подписка действительна
        if expiration_date > datetime.now().date():
            password = await get_account_password(account_email)
            # Обрабатываем индивидуальный аккаунт (удаляем суффикс "_ind")
            account_email_display = f"<code>{account_email[:-4]}</code>" if account_email.endswith(
                '_ind') else f"<code>{account_email}</code>"
        else:
            password = None
            account_email_display = 'У вас нет активного аккаунта ChatGPT'
        # Форматируем дату окончания подписки
        formatted_expiration_date = expiration_date.strftime('%d.%m.%Y')
    else:
        password = None
        account_email_display = 'У вас нет активного аккаунта ChatGPT'
        formatted_expiration_date = 'Подписка не активна'

    # Проверка наличия резервного аккаунта
    if await check_user_backup_account(user_id):
        email_backup_account = await get_user_backup_account(user_id)
        backup_account_password = await get_backup_account_password(email_backup_account)
        backup_account_inf = (
            f"\n\n<b>=============================</b>\n"
            f"<b><i>Резервный аккаунт:</i></b>\n\n"
            f"<b>Логин:</b> <code>{email_backup_account}</code>\n"
            f"<b>Пароль:</b> <code>{backup_account_password}</code>\n\n"
            f"<b>=============================</b>"
        )

    # Собираем текст сообщения профиля
    profile_text = (
        f"<b>Дата окончания подписки:</b> <u>{formatted_expiration_date}</u>\n\n"
        f"🪪 <b>Логин ChatGPT:</b> {account_email_display}\n"
        f"<b>🔐 Пароль:</b> {f'<code>{password}</code>' if password else 'нет действующего пароля'}"
        f"{backup_account_inf}"
    )
    # Если аккаунт индивидуальный, то не даем возможности запросить резервный аккаунт
    if account_is_ind:
        await bot.edit_message_text(chat_id=message.chat.id,
                                    message_id=message.message_id,
                                    text=profile_text,
                                    parse_mode=ParseMode.HTML, reply_markup=back_to_menu_inline_kb())
    else:

        await bot.edit_message_text(chat_id=message.chat.id,
                                    message_id=message.message_id,
                                    text=profile_text,
                                    reply_markup=requests_have_ended_inline_kb(),
                                    parse_mode=ParseMode.HTML)


# Обработчик запроса на резервный аккаунт
@router.callback_query(F.data == "req_have_ended")
async def req_have_ended(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id

    # Получаем данные о сроке подписки и последнем запросе на резервный аккаунт
    date_expiration = await get_user_expiration_date(user_id)
    expiration_valid = date_expiration and datetime.strptime(date_expiration.strip(),
                                                             '%Y-%m-%d').date() > datetime.now().date()

    used_backup_account_date = await get_used_backup_account_date(user_id)
    backup_available = True

    if used_backup_account_date:
        used_backup_account_date = datetime.strptime(used_backup_account_date.strip(), '%Y-%m-%d %H:%M:%S')
        if used_backup_account_date + timedelta(days=3) > datetime.now():
            backup_available = False

    if not expiration_valid:
        backup_available = False

    # Текст сообщения с учетом условий
    text = (
        "Если у Вас исчерпан лимит запросов, вы можете получить временный резервный аккаунт. "
        "Данные от него будут доступны в профиле в течение 1 дня.\n"
        "После нажатия кнопки она будет недоступна следующие 3 дня."
        if backup_available else
        "Вы уже запрашивали резервный аккаунт. Кнопка станет доступна через 3 дня."
    )

    # Отправляем сообщение с кнопкой
    await bot.edit_message_text(chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                text=text,
                                reply_markup=backup_account_inline_kb(backup_available))
