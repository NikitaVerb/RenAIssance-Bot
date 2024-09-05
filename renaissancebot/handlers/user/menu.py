from aiogram import Router, F, Bot
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from keyboards import main_inline_kb

router = Router()


@router.callback_query(F.data.startswith('menu'))
async def menu(callback: CallbackQuery, bot: Bot):
    await bot.edit_message_text(chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id, text='Выберите интересующий раздел👇🏻',
                                parse_mode=ParseMode.MARKDOWN, reply_markup=main_inline_kb())
