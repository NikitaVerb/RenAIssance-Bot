from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from keyboards import main_inline_kb

router = Router()


async def menu(message: Message):
    await message.answer(
        'Выберите интересующий раздел👇🏻',
        reply_markup=main_inline_kb())


@router.callback_query(F.data.startswith('menu'))
async def callback_menu(callback: CallbackQuery):
    await callback.answer()
    await menu(callback.message)
