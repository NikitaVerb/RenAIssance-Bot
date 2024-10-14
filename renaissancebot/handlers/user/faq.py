from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from keyboards import faq_inline_kb, back_to_faq_inline_kb

router = Router()


@router.callback_query(F.data == "faq")
async def faq_handler(callback: CallbackQuery, bot: Bot):
    await bot.edit_message_text(chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id, text="Выберите тему для получения помощи:",
                                reply_markup=faq_inline_kb())


@router.callback_query(F.data.startswith('faq_'))
async def faq_question(callback: CallbackQuery, bot: Bot):
    question = int(callback.data.split('_')[1])
    match question:
        case 1:
            text = ("🫂 Вы получаете полный доступ к функционалу платной подписки,"
                    " разделяя аккаунт с небольшим количеством пользователей.")
        case 2:
            text = ("🔥 Качественный сервис, низкая загруженность аккаунтов, довольные клиенты - это все про нас!")
        case 3:
            text = ("🧑‍💻 Конечно, если аккаунты модерировать и не перегружать."
                    " К тому же, на всякий случай, у нас всегда припасены резервные аккаунты, на которых постоянно есть запросы."
                    " Они входят в стоимость подписки и доступны в профиле.")
        case 4:
            text = ("⏰ Вы можете выбрать один из трех периодов:"
                    " 1/3/6 месяцев. По истечению (считается со дня покупки) нужно будет произвести новую оплату, чтобы продлить подписку.")
        case 5:
            text = ("🥷 Если ваш регион заблокирован, то нужно включить VPN."
                    " Рекомендуем подключаться к американским серверам.")
        case _:
            text = '12'

    await bot.edit_message_text(chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id, text=text, reply_markup=back_to_faq_inline_kb())
