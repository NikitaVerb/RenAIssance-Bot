from datetime import datetime, timedelta

from aiogram import Router, types, F, Bot
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from db import get_user_account, get_user_expiration_date, get_account_password, \
    get_used_backup_account_date, get_user_backup_account, get_backup_account_password, check_user_in_db, \
    check_user_backup_account
from keyboards import backup_account_inline_kb, requests_have_ended_inline_kb, \
    reg_from_profile_inline_markup, back_to_menu_inline_kb, menu_and_catalog_inline_kb

router = Router()


# Обработчик callback'а для команды профиля
@router.callback_query(F.data.startswith('profile'))
async def profile(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id

    # Проверка, зарегистрирован ли пользователь
    if not await check_user_in_db(user_id):
        await bot.edit_message_text(chat_id=callback.message.chat.id,
                                    message_id=callback.message.message_id,
                                    text='Для покупки подписки и отслеживания её статуса необходимо зарегистрироваться.',
                                    reply_markup=reg_from_profile_inline_markup())
        return


    # Проверка активна ли подписка у пользователя
    msg = bot.edit_message_text(chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id,
                                text='На данный момент у вас нет активной подписки.'
                                     ' Статус подписки можно посмотреть только, если она действительна.',
                                reply_markup=menu_and_catalog_inline_kb())

    expiration_date = await get_user_expiration_date(user_id)
    if not expiration_date:
        await msg
        return
    elif datetime.strptime(expiration_date, '%Y-%m-%d').date() < datetime.now().date():
        await msg
        return

    await profile_handler(callback.message, user_id, bot)


async def profile_handler(message: types.Message, user_id: int, bot: Bot):
    # Получаем основные данные пользователя
    account_email = await get_user_account(user_id)
    expiration_date = datetime.strptime(await get_user_expiration_date(user_id), '%Y-%m-%d').date()
    backup_account_inf = ''

    account_is_ind = (account_email and account_email.endswith('_ind'))
    # Проверяем срок действия подписки

    password = await get_account_password(account_email)
    # Обрабатываем индивидуальный аккаунт (удаляем суффикс "_ind")
    account_email_display = f"<code>{account_email[:-4]}</code>" if account_email.endswith(
        '_ind') else f"<code>{account_email}</code>"

    # Форматируем дату окончания подписки
    formatted_expiration_date = expiration_date.strftime('%d.%m.%Y')

    # Проверка наличия резервного аккаунта
    if await check_user_backup_account(user_id):
        email_backup_account = await get_user_backup_account(user_id)
        backup_account_password = await get_backup_account_password(email_backup_account)
        backup_account_inf = (
            f"\n\n<b>=============================</b>\n"
            f"<b><i>Резервный аккаунт:</i></b>\n\n"
            f"<b><i>Логин:</i></b> <code>{email_backup_account}</code>\n"
            f"<b><i>Пароль:</i></b> <code>{backup_account_password}</code>\n\n"
            f"<b>=============================</b>"
        )

    # Собираем текст сообщения профиля
    profile_text = (
        f"<b>Дата окончания подписки:</b> <u>{formatted_expiration_date}</u>\n\n"
        f"🪪 <b>Логин ChatGPT:</b> {account_email_display} \n"
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
        "Если исчерпался лимит, у нас есть для Вас резервный аккаунт с запросами."
        " Он будет доступен в течение 1 дня. После нажатия кнопка будет заблокирована на 3 дня."
        if backup_available else
        "Вы уже запрашивали резервный аккаунт. Функция будет доступна через 3 дня."
    )

    # Отправляем сообщение с кнопкой
    await bot.edit_message_text(chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                text=text,
                                reply_markup=backup_account_inline_kb(backup_available))
