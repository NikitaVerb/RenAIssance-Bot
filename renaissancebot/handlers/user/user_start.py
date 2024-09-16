from aiogram import Router
from aiogram import types
from aiogram.enums import ParseMode
from aiogram.filters import Command

from keyboards import main_inline_kb

router = Router()


@router.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer('Выберите интересующий раздел👇🏻',
                         parse_mode=ParseMode.MARKDOWN, reply_markup=main_inline_kb())
