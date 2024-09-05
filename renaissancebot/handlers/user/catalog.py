from aiogram import Router, F, Bot
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from keyboards import catalog_navigation_inline_kb

router = Router()


@router.callback_query(F.data.startswith('catalog'))
async def catalog(callback: CallbackQuery, bot: Bot):
    await bot.edit_message_text(chat_id=callback.message.chat.id,
        message_id=callback.message.message_id, text=
    '<b>DECA - 649/месяц.</b>\n\nCовместный аккаунт до 7 человек с ChatGPT-4 (Plus).'
    ' Активно модерируется, чтобы всем хватало запросов. Комфорт и эффективность в одном тарифе.',
                                parse_mode=ParseMode.HTML, reply_markup=catalog_navigation_inline_kb(2, 1))


@router.callback_query(F.data.startswith("navigation_"))
async def catalog_process(callback: CallbackQuery, bot: Bot):
    await callback.answer()
    page = int(callback.data.split("_")[1])

    match page:
        case 1:
            text = ("<b>DECA - 649/месяц.</b>\n\nШеринговый аккаунт до 7 человек."
                    " Активно модерируется, чтобы всем хватало запросов. Комфорт и эффективность в одном тарифе."
                    " Самый частый выбор наших клиентов.")
        case 2:
            text = ("<b>UNICO - 2500/месяц.</b>\n\nИндивидуальный аккаунт, который будет доступен только вам."
                    " Вы получите полный доступ к функционалу ChatGPT-4. Оставьте заявку, чтобы приобрести.")
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
