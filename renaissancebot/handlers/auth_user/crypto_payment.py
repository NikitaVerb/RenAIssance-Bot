from datetime import datetime

from aiogram import Bot, Router, types
from aiogram import F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram.types import ContentType

from db import set_expiration_date, set_purchase_date, get_user_expiration_date, \
    add_link_user_to_account, get_user_account, get_most_linked_email_account, get_all_admin_ids, add_to_users_spent, \
    set_notified, get_user_email, unlink_user_from_account, reset_used_backup_account, remove_backup_account
from filters.user_data_callback_factory import UserDataCallbackFactory
from handlers.admin.send_message_to_all_admins import send_message_to_all_admins
from handlers.auth_user.pay import add_months
from keyboards import profile_button_inline_kb, admin_approval_inline_kb, back_to_catalog_inline_kb
from keyboards.support_inline_kb import support_inline_kb

router = Router()


# Состояния FSM для процесса обработки фото или ссылки
class PurchaseFSM(StatesGroup):
    waiting_for_photo_or_link = State()
    waiting_for_admin_decision = State()


# Хэндлер для обработки callback'а "crypto"
@router.callback_query(F.data == "crypto")
async def handle_crypto_callback(callback: CallbackQuery, state: FSMContext, bot: Bot):
    user_data = await state.get_data()
    months = user_data.get("subscription_months")
    match months:
        case "1":
            price = 7
        case "3":
            price = 19
        case "6":
            price = 36
        case "ind":
            price = 28
        case _:
            price = 0
    # Изменяем сообщение на другое (текст потом можно подставить)

    await bot.edit_message_text(chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id,
                                text=f"Переведите ${price} по адресу, указанному ниже,"
                                     f" после чего отправьте скриншот с транзакцией либо ссылку на неё в чат."
                                     f" Чтобы прервать процесс оплаты, отправьте команду /cancel в чат.\n\n"
                                     f"USDT (BEP-20): <code>0x585c6b8cD5dB299dbDE3fA9bfB28175bB2d75655</code>"
                                     f" (нажмите, чтобы скопировать)\n\n"
                                     f"USDT (TRC-20): <code>TAh5bPQVhWCQKKKoi5qjL1CNuvJFzigNe6</code>"
                                     f" (нажмите, чтобы скопировать)")

    # Переходим в состояние ожидания фотографии или ссылки
    await state.update_data(amount=price * 91)
    await state.set_state(PurchaseFSM.waiting_for_photo_or_link)


# Обработка фото или ссылки от пользователя
@router.message(PurchaseFSM.waiting_for_photo_or_link, F.content_type.in_([ContentType.PHOTO, ContentType.TEXT]))
async def process_photo_or_link(message: types.Message, state: FSMContext, bot: Bot):
    if message.text == "/cancel":
        await state.clear()
        await message.answer("Процесс оплаты прерван", reply_markup=back_to_catalog_inline_kb())
        return
    user_data = {}
    user_email = await get_user_email(message.from_user.id)
    data = await state.get_data()
    sub_type = data.get("subscription_months")
    amount = int(data.get("amount", 0))
    if sub_type == "ind":
        admin_message = (
            f"Пользователь {user_email} отправил подтверждение на оплату индивидуального аккаунта на месяц."
            f" Проверьте и примите решение:")
    else:
        admin_message = (f"Пользователь {user_email} отправил подтверждение на плату аккаунта на {sub_type} мес."
                         f" Проверьте и примите решение:")

    if message.photo:
        # Если пришло фото, сохраняем файл
        user_data['photo'] = message.photo[-1].file_id  # Берём самое большое фото
        # Отправляем сообщение админу с кнопками
        for admin_id in await get_all_admin_ids():
            await bot.send_photo(admin_id, photo=user_data['photo'], caption=admin_message,
                                 reply_markup=admin_approval_inline_kb(user_id=message.from_user.id,
                                                                       sub_type=sub_type,
                                                                       amount=amount))
    elif message.text:
        # Если пришла ссылка
        user_data['link'] = message.text
        admin_message += message.text
        for admin_id in await get_all_admin_ids():
            await bot.send_message(admin_id, text=admin_message,
                                   reply_markup=admin_approval_inline_kb(user_id=message.from_user.id,
                                                                         sub_type=sub_type,
                                                                         amount=amount))

    # Сохраняем фото или ссылку в состояние
    await state.update_data(**user_data)

    await state.update_data(user_id=message.from_user.id)
    await message.answer("Ваша транзакция была отправлена администратору на проверку."
                         " После подтверждения Вы получите уведомление.")
    # Переходим в состояние ожидания решения от админа
    await state.set_state(PurchaseFSM.waiting_for_admin_decision)


# Обработка решения админа: одобрить
@router.callback_query(UserDataCallbackFactory.filter())
async def admin_approve(callback: types.CallbackQuery, callback_data: UserDataCallbackFactory, bot: Bot):
    await callback.answer()
    # Удаление клавиатуры у сообщения
    await callback.message.edit_reply_markup(reply_markup=None)

    # Извлечение данных
    user_id = callback_data.user_id
    months = callback_data.subscription_type
    amount = callback_data.amount

    if callback_data.action == "problem":
        await callback.answer()
        # Удаляем клавиатуру
        await callback.message.edit_reply_markup(reply_markup=None)
        # Отправляем пользователю сообщение о проблеме с кнопкой для связи с поддержкой
        await bot.send_message(user_id, "Произошла проблема с вашим платежом. Пожалуйста, свяжитесь с поддержкой.",
                               reply_markup=support_inline_kb())
        return

    user_email = await get_user_email(user_id)
    if months == "ind":
        await bot.send_message(user_id, "Успешная оплата. Спасибо за покупку!\n\n"
                                        f"Мы уже оформляем подписку. Аккаунт в скором времени отобразится в Вашем профиле."
                                        f" Мы оповестим Вас, когда это произойдёт.\n\n"
                                        f"Подписывайтесь на <a href='https://t.me/plusgpt4'>телеграм-канал</a>,"
                                        f" чтобы оставаться в курсе событий.",
                               reply_markup=profile_button_inline_kb())
        await send_message_to_all_admins(bot=bot,
                                         message_text=f"Юзер {user_email} оплатил подписку на индивидуальный аккаунт на месяц.")
        await add_to_users_spent(callback.message.from_user.id, amount)
        return
    else:
        months = int(months)

    if not user_id or not months:
        await callback.message.answer("Ошибка: не удалось получить данные пользователя или количество месяцев.")
        return

    # Сообщение пользователю об успешном завершении проверки
    msg = (f'Администратор подтвердил ваш платёж. Спасибо за покупку!\n'
           f'Откройте профиль, чтобы получить аккаунт.\n\n'
           f'Подписывайтесь на <a href="https://t.me/plusgpt4">телеграм-канал</a>, чтобы оставаться в курсе событий.')

    # Получаем текущую дату окончания подписки
    user_expiration_date = await get_user_expiration_date(user_id)
    if user_expiration_date:
        user_expiration_date = datetime.strptime(user_expiration_date.strip(), '%Y-%m-%d').date()
        if user_expiration_date > datetime.now().date():
            user_expiration_date = add_months(user_expiration_date, months)
        else:
            user_expiration_date = add_months(datetime.now(), months)
    else:
        user_expiration_date = add_months(datetime.now(), months)

    # Получаем аккаунт пользователя, если аккаунт еще не привязан, назначаем его
    account_email = await get_user_account(user_id)
    if not account_email or account_email.endswith('_ind'):
        account_email = await get_most_linked_email_account()
        await unlink_user_from_account(user_id)
        await add_link_user_to_account(user_id, account_email)

    # Обновляем дату окончания подписки
    await set_expiration_date(user_id, str(user_expiration_date))

    # Устанавливаем дату покупки
    purchase_date = datetime.now().date()
    await set_purchase_date(user_id, str(purchase_date))

    # Обновляем информацию о затратах пользователя
    await add_to_users_spent(user_id, amount)

    # Устанавливаем значение notified в 0 (чтобы пользователь получил уведомление о продлении)
    await set_notified(user_id, 0)

    # сброс времени последней активации резервного аккаунта
    await reset_used_backup_account(user_id)
    await remove_backup_account(user_id)

    # Отправляем сообщение пользователю
    await bot.send_message(user_id, msg, reply_markup=profile_button_inline_kb(), parse_mode=ParseMode.HTML)
