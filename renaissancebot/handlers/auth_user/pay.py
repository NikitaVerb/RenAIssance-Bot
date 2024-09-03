from datetime import datetime, timedelta

from aiogram import Bot, Router, F
from aiogram.types import LabeledPrice, PreCheckoutQuery, Message, CallbackQuery

import renaissancebot.filters.user_rights
from db import get_user_expiration_date, get_most_linked_email_account, add_link_user_to_account, get_user_account
from db import set_expiration_date, set_purchase_date, add_to_spent, check_user_in_db
from keyboards import reg_inline_markup

router = Router()
router.message.filter(renaissancebot.filters.user_rights.UserIsLogged())


# Обработчик команды для оформления заказа
@router.callback_query(F.data.startswith('subscribe_'))
async def order(callback: CallbackQuery, bot: Bot):
    await callback.answer()
    if not (await check_user_in_db(callback.from_user.id)):
        await callback.message.answer(
            f'Если хотите приобрести подписку или отслеживать статус уже купленной подписки,'
            f' то вам нужно зарегистрироваться',
            reply_markup=reg_inline_markup())
        return

    month = int(callback.data.split('_')[1])
    price = 0
    description = ''
    match month:
        case 1:
            price = 10000
            description = 'Подписка ChatGPT+ на 1 месяц'
        case 3:
            price = 15000
            description = 'Подписка ChatGPT+ на 3 месяца'
        case 6:
            price = 25000
            description = 'Подписка ChatGPT+ на 6 месяцев'
    await bot.send_invoice(
        chat_id=callback.message.chat.id,
        title='Покупка подписки',
        description=description,
        payload=f'subscription_{month}_months',  # Уникальный идентификатор платежа с количеством месяцев
        provider_token='381764678:TEST:93996',  # Тестовый токен платежного провайдера
        currency='RUB',
        prices=[
            LabeledPrice(
                label='Доступ к подписке',
                amount=price,  # Цена в копейках (10000 копеек = 100 рублей)
            )
        ],
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
async def success_payment(message: Message):
    amount = message.successful_payment.total_amount // 100  # Сумма в рублях
    currency = message.successful_payment.currency
    msg = (f'Спасибо за оплату {amount} {currency}!\n'
           f'Откройте профиль командой /profile, там будет отображаться вся актуальная информация, аккаунт ChatGPT+ и пароль от аккаунта')

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
    if not account_email:
        account_email = await get_most_linked_email_account()
        await add_link_user_to_account(message.from_user.id, account_email)

    # Установка новой даты окончания подписки
    await set_expiration_date(message.from_user.id, str(user_expiration_date))

    # Установка даты покупки
    purchase_date = datetime.now().date()
    await set_purchase_date(message.from_user.id, str(purchase_date))

    # Обновление потраченной суммы (spent)
    await add_to_spent(message.from_user.id, amount)

    await message.answer(msg)
