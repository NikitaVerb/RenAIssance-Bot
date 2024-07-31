from aiogram import Router
from aiogram import types
from aiogram.filters import Command
router = Router()

users = [988750689]


@router.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer(f'Hi, {message.from_user.full_name}, id: {message.from_user.id}')



