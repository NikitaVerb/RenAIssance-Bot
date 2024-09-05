from aiogram import Router, F
from aiogram import types
from aiogram.enums import ParseMode
from aiogram.filters import Command

from filters.user_rights import UserIsLogged
from keyboards import reg_inline_markup, main_inline_kb

router = Router()


@router.message(Command('start'))
async def cmd_start(message: types.Message):
    if not UserIsLogged():
        await message.answer(
            f'Если хотите приобрести подписку или отслеживать статус уже купленной подписки,'
            f' то вам нужно зарегестрироваться'
            , reply_markup=reg_inline_markup())
    await message.answer('Выберите интересующий раздел👇🏻',
                         parse_mode=ParseMode.MARKDOWN, reply_markup=main_inline_kb())


@router.message(F.text == "Связаться")
async def send_contact(message: types.Message):
    await message.answer("@RenAIssanceSupport")
    await message.delete()


@router.message(F.text == 'Наш телеграм-канал🤖')
async def send_tg_contact(message: types.Message):
    await message.answer("<a href='https://t.me/plusgpt4'>https://t.me/plusgpt4</a>")
    await message.delete()
