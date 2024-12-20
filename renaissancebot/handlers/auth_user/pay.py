from datetime import datetime, timedelta

from aiogram import Bot, Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import LabeledPrice, PreCheckoutQuery, Message, CallbackQuery

import filters.user_rights
from config_reader import config
from db import get_user_expiration_date, get_most_linked_email_account, add_link_user_to_account, get_user_account, \
    get_user_email, unlink_user_from_account, reset_used_backup_account, remove_backup_account
from db import set_expiration_date, set_purchase_date, add_to_users_spent, check_user_in_db
from db.users.set_notified import set_notified
from handlers.admin.send_message_to_all_admins import send_message_to_all_admins
from keyboards import reg_from_catalog_inline_markup, back_to_catalog_inline_kb, \
    profile_button_inline_kb
from keyboards.payment_method_inline_kb import payment_method_inline_kb

router = Router()
router.message.filter(filters.user_rights.UserIsLogged())


# Обработчик команды для оформления заказа
@router.callback_query(F.data.startswith('subscribe_'))
async def order(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.answer()

    months = (callback.data.split('_')[1])
    # Сохраняем информацию о месячном плане в состоянии
    await state.update_data(subscription_months=months)

    if not (await check_user_in_db(callback.from_user.id)):
        await bot.edit_message_text(chat_id=callback.message.chat.id,
                                    message_id=callback.message.message_id, text=
                                    f'Если хотите приобрести подписку или отслеживать статус уже купленной подписки,'
                                    f' то вам нужно зарегистрироваться.',
                                    reply_markup=reg_from_catalog_inline_markup(pay=True))

        return

    if not (await get_most_linked_email_account()):
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                    text="Извините, к сожалению, у нас сейчас нет свободных аккаунтов",
                                    reply_markup=back_to_catalog_inline_kb())
        return
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                text="Выберите удобный Вам способ оплаты", reply_markup=payment_method_inline_kb())


@router.callback_query(F.data == "invoice")
async def invoice_handler(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    months = data.get("subscription_months")
    await send_invoice(callback.message, bot, months)


async def send_invoice(message: Message, bot: Bot, months: str):
    # Определяем цену и описание в зависимости от количества месяцев
    match months:
        case "1":
            price = 64900
            description = 'Совместный аккаунт «DECA»'
            tariff = 'DECA'
        case "3":
            price = 174900
            description = 'Совместный аккаунт «DECA»'
            tariff = 'DECA'
        case "6":
            price = 334900
            description = 'Совместный аккаунт «DECA»'
            tariff = 'DECA'
        case "ind":
            price = 250000
            description = 'Индивидуальный аккаунт «UNICO» — 1 месяц'
            tariff = 'UNICO'
        case _:
            price = 0
            description = ''
            tariff = ''
    # Отправляем инвойс
    await bot.send_invoice(
        chat_id=message.chat.id,
        title='Покупка подписки (карта РФ)',
        description=description,
        payload=f'subscription_{months}',  # Информация о подписке
        provider_token=config.provider_token.get_secret_value(),
        currency='RUB',
        prices=[LabeledPrice(label=f'Тариф {tariff}', amount=price)],
        start_parameter='subscription_start',
        provider_data=None,
        photo_url=None,
        request_timeout=15
    )


# Обработчик предварительного запроса на оплату
@router.pre_checkout_query()
async def pre_checkout_query(pr_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query_id=pr_query.id, ok=True)


def add_months(source_date, months):
    # Рассчитываем новый месяц и год
    month = source_date.month - 1 + months
    year = source_date.year + month // 12
    month = month % 12 + 1

    # Определяем последний день месяца
    day = min(
        source_date.day,
        (datetime(year, month % 12 + 1, 1) - timedelta(days=1)).day
    )

    return datetime(year, month, day).date()


@router.message(F.successful_payment)
async def success_payment(message: Message, bot: Bot):
    amount = message.successful_payment.total_amount // 100  # Сумма в рублях
    user_id = message.from_user.id
    # Извлечение количества месяцев из payload
    payload = message.successful_payment.invoice_payload
    months = payload.split('_')[1]
    if months == "ind":
        await message.answer(f"Успешная оплата. Спасибо за покупку!\n\n"
                             f"Мы уже оформляем подписку. Аккаунт в скором времени отобразится в Вашем профиле."
                             f" Мы оповестим Вас, когда это произойдёт.\n\n"
                             f"Подписывайтесь на <a href='https://t.me/plusgpt4'>телеграм-канал</a>,"
                             f" чтобы оставаться в курсе событий.", reply_markup=profile_button_inline_kb())
        await send_message_to_all_admins(bot=bot, message_text=f"Юзер {await get_user_email(message.from_user.id)}"
                                                               " оплатил подписку"
                                                               f" на индивидуальный аккаунт на месяц")
        await add_to_users_spent(message.from_user.id, amount)
        return

    msg = (f'Успешная оплата. Спасибо за покупку!\n'
           f'Откройте профиль, чтобы получить аккаунт.\n\n'
           f'Подписывайтесь на <a href="https://t.me/plusgpt4">телеграм-канал</a>, чтобы оставаться в курсе событий.')

    # Извлечение количества месяцев из payload
    months = int(message.successful_payment.invoice_payload.split('_')[1])

    # Обновление даты окончания подписки
    user_expiration_date = await get_user_expiration_date(message.chat.id)
    if user_expiration_date:
        user_expiration_date = datetime.strptime(user_expiration_date.strip(), '%Y-%m-%d').date()
        if user_expiration_date > datetime.now().date():
            user_expiration_date = add_months(user_expiration_date, months)
        else:
            user_expiration_date = add_months(datetime.now(), months)
    else:
        user_expiration_date = add_months(datetime.now(), months)

    # Проверка наличия аккаунта и связывание с пользователем при необходимости
    account_email = await get_user_account(message.from_user.id)
    if not account_email or account_email.endswith("_ind"):
        account_email = await get_most_linked_email_account()
        await unlink_user_from_account(message.from_user.id)
        await add_link_user_to_account(message.from_user.id, account_email)

    # Установка новой даты окончания подписки
    await set_expiration_date(message.from_user.id, str(user_expiration_date))

    # Установка даты покупки
    purchase_date = datetime.now().date()
    await set_purchase_date(message.from_user.id, str(purchase_date))

    # Обновление потраченной суммы (spent)
    await add_to_users_spent(message.from_user.id, amount)

    #сброс времени последней активации резервного аккаунта
    await reset_used_backup_account(user_id)
    await remove_backup_account(user_id)
    # Устанавливаем значение notified в 0, что означает, что пользователь не оповещен о продлении подписки
    await set_notified(message.from_user.id, 0)
    await message.answer(msg, reply_markup=profile_button_inline_kb(), parse_mode=ParseMode.HTML)
