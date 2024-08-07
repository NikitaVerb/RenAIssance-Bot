from aiogram import Router
from aiogram import types
from aiogram.filters import Command

from keyboards import reg_inline_markup, get_main_kb

router = Router()


@router.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer(
        f'Если хотите приобрести подписку или отслеживать статус уже купленной подписки,'
        f' то вам нужно зарегестрироваться'
        , reply_markup=reg_inline_markup())
    await message.answer(reply_markup=get_main_kb())
    await message.answer(
        'Если хотите посмотреть каталог, наш телеграм-канал или задать вопрос, воспользуйтесь кнопками под клавиатурой',
        reply_markup=get_main_kb())
    # TODO await message.answer("Каталог", reply_markup=catalog_inline_markup())
