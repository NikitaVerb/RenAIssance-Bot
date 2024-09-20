import logging
from datetime import datetime

from aiogram import Router, types, Bot
from aiogram.filters import Command, CommandObject

import filters.user_rights
from db import check_account_in_db, check_user_email_in_db, get_user_id, \
    add_link_user_to_account, set_expiration_date, set_purchase_date, \
    get_user_expiration_date, unlink_user_from_account
from db.users.set_notified import set_notified
from keyboards import profile_button_inline_kb

router = Router()
router.message.filter(filters.user_rights.UserIsAdmin())


@router.message(Command('link'))
async def link_user_to_account_handler(message: types.Message, command: CommandObject, bot: Bot):
    try:
        # Проверяем, что переданы аргументы
        if not command.args:
            await message.answer(
                "Неправильный формат команды. Используйте: /link <account_email> <user_email> <expiration_date(yyyy-mm-dd)>")
            return

        # Получаем аргументы
        args = command.args.split()

        # Должно быть минимум 2 аргумента
        if len(args) < 2:
            await message.answer(
                "Неправильный формат команды. Используйте: /link <account_email> <user_email> <expiration_date(yyyy-mm-dd)>")
            return

        account_email = args[0]
        user_email = args[1]

        # Если передан третий аргумент, используем его как дату окончания подписки
        if len(args) == 3:
            expiration_date = args[2]
            try:
                # Проверяем правильность формата даты
                expiration_date = datetime.strptime(expiration_date.strip(), '%Y-%m-%d').date()
            except ValueError:
                await message.answer('Неверный формат даты. Используйте формат ГГГГ-ММ-ДД.')
                return
        else:
            # Если третий аргумент не передан, проверяем, есть ли дата окончания подписки у пользователя
            user_id = int(await get_user_id(user_email))
            expiration_date = await get_user_expiration_date(user_id)
            if expiration_date is None:
                await message.answer(
                    "У пользователя нет даты окончания подписки. Неправильный формат команды. Используйте: "
                    "/link <account_email> <user_email> <expiration_date(yyyy-mm-dd)>", parse_mode=None)
                return

        # Проверяем, существует ли аккаунт в базе
        if not await check_account_in_db(account_email):
            await message.answer("Такого аккаунта нет в базе")
            return

        # Получаем user_id по email пользователя
        user_id = await get_user_id(user_email)
        if user_id is None:
            await message.answer("Пользователь с таким email не найден")
            return
        user_id = int(user_id)

        # Проверяем, существует ли email пользователя в базе
        if not await check_user_email_in_db(user_email):
            await message.answer("Пользователь с таким email не найден")
            return

        # Отвязываем пользователя от текущих аккаунтов, если есть
        await unlink_user_from_account(user_id)

        # Привязываем пользователя к новому аккаунту
        await add_link_user_to_account(user_id, account_email)

        # Устанавливаем дату окончания подписки и дату покупки
        await set_expiration_date(user_id, expiration_date)
        purchase_date = datetime.now().date()
        await set_purchase_date(user_id, str(purchase_date))

        # Уведомляем о успешной привязке
        await message.answer(
            f"Пользователь {user_email} успешно привязан к аккаунту {account_email} до {expiration_date}.")

        if user_email.endswith('_ind'):
            # уведомляем владельца индивидуального аккаунта, что он теперь привязан к аккаунту
            await bot.send_message(chat_id=user_id, text="Ваш индивидуальный аккаунт готов! Информацию"
                                                         " об аккаунте вы можете посмотреть в профиле.",
                                   reply_markup=profile_button_inline_kb())
        # Устанавливаем значение notified в 0, что означает, что пользователь не оповещен о продлении подписки
        await set_notified(user_id, 0)

    except Exception as e:
        # Логируем и отправляем уведомление об ошибке
        await message.answer("Произошла ошибка при привязывании пользователя к аккаунту")
        logging.exception(e)
