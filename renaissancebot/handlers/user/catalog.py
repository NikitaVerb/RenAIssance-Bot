from aiogram import Router, F, Bot
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery, InputMediaPhoto

from keyboards import catalog_navigation_inline_kb

router = Router()


@router.message(F.text == 'Каталог')
async def catalog(message: Message):
    photo_id = "AgACAgIAAxkBAAIDimazVhnKFOzxUYp5kKNqymkbpsUaAAK64DEb49-YSejBOi7eNYlWAQADAgADeAADNQQ"
    await message.answer_photo(photo=photo_id, caption='<b>DECA - 649/месяц.</b>\n\nШеринговый аккаунт до 7 человек.'
                                                       'Активно модерируется, чтобы всем хватало запросов. Комфорт '
                                                       'и эффективность в одном тарифе. Самый частый выбор наших клиентов',
                               parse_mode=ParseMode.HTML, reply_markup=catalog_navigation_inline_kb(2, 1))


@router.callback_query(F.data.startswith("navigation_"))
async def catalog_process(callback: CallbackQuery, bot: Bot):
    await callback.answer()
    page = int(callback.data.split("_")[1])
    photo_id = "AgACAgIAAxkBAAIDimazVhnKFOzxUYp5kKNqymkbpsUaAAK64DEb49-YSejBOi7eNYlWAQADAgADeAADNQQ"
    match page:
        case 1:
            text = ("<b>DECA - 649/месяц.</b>\n\nШеринговый аккаунт до 7 человек."
                    " Активно модерируется, чтобы всем хватало запросов. Комфорт и эффективность в одном тарифе."
                    " Самый частый выбор наших клиентов.")
        case 2:
            text = ("<b>UNICO - 2500/месяц.</b>\n\nИндивидуальный аккаунт, который будет доступен только вам."
                    " Вы получите полный доступ к функционалу ChatGPT-4.")
        case _:
            text = 'Произошла ошибка'
    await bot.edit_message_media(chat_id=callback.message.chat.id,
                                 message_id=callback.message.message_id,
                                 media=InputMediaPhoto(media=photo_id, caption=text),
                                 reply_markup=catalog_navigation_inline_kb(2, page))


@router.callback_query(F.data == 'pass')
async def pass_callback(callback: CallbackQuery):
    await callback.answer()
