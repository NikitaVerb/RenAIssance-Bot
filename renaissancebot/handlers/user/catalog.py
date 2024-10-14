from aiogram import Router, F, Bot
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from keyboards import catalog_navigation_inline_kb

router = Router()


@router.callback_query(F.data.startswith('catalog'))
async def catalog(callback: CallbackQuery, bot: Bot):
    await bot.edit_message_text(chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id, text=(
            "<b>🌐 Тариф DECA — 1/3/6 месяцев.</b>\n\nCовместный аккаунт до 7 человек с ChatGPT-4 (Plus)."
            " Активно модерируется, чтобы всем хватало запросов."
            " Комфорт и эффективность в одном тарифе.\n\n"
            "Вы получаете логин и пароль от аккаунта, с которыми заходите на официальный сайт chatgpt.com. "
            "После истечения выбранного срока следует новая оплата.\n\n"
            "Гарантия действует на все время подписки."),
                                parse_mode=ParseMode.HTML, reply_markup=catalog_navigation_inline_kb(2, 1))


@router.callback_query(F.data.startswith("navigation_"))
async def catalog_process(callback: CallbackQuery, bot: Bot):
    await callback.answer()
    page = int(callback.data.split("_")[1])

    match page:
        case 1:
            text = ("<b>🌐 Тариф DECA — 1/3/6 месяцев.</b>\n\nCовместный аккаунт до 7 человек с ChatGPT-4 (Plus)."
                    " Активно модерируется, чтобы всем хватало запросов."
                    " Комфорт и эффективность в одном тарифе.\n\n"
                    "Вы получаете логин и пароль от аккаунта, с которыми заходите на официальный сайт chatgpt.com. "
                    "После истечения выбранного срока следует новая оплата.\n\n"
                    "Гарантия действует на все время подписки.")
        case 2:
            text = ("<b>👑 Тариф UNICO — 1 месяц</b>\n\nИндивидуальный аккаунт, который будет доступен только Вам."
                    " Полный доступ к функционалу ChatGPT-4. Для тех, кто предпочитает оставаться непубличным.\n\n"
                    "После оплаты мы быстро оформляем подписку на отдельный аккаунт, после чего Вы получаете логин и пароль,"
                    "с которыми заходите на официальный сайт chatgpt.com.\n\n"
                    "Гарантия действует на всё время подписки.")
        case _:
            text = 'Произошла ошибка'

    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=catalog_navigation_inline_kb(2, page)
    )


@router.callback_query(F.data == 'pass')
async def pass_callback(callback: CallbackQuery):
    await callback.answer()
