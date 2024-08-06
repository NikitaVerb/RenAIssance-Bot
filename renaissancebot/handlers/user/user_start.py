from aiogram import Router
from aiogram import types
from aiogram.filters import Command
from keyboards import reg_inline_markup

router = Router()


@router.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer(f'Hi, {message.from_user.full_name}, id: {message.from_user.id} chat_id: {message.chat.id}')
    await message.answer(
        f'Если хотите приобрести подписку или отслеживать статус уже купленной подписки, то вам нужно зарегестрироваться'
    , reply_markup=reg_inline_markup())


