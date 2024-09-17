from aiogram import Router, F, types

router = Router()


@router.message(F.text == 'id')
async def send_text_id(message: types.Message):
    await message.answer(str(message.from_user.id))
