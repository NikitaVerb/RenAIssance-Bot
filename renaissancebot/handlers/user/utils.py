from aiogram import Router, F, types

router = Router()


@router.message(F.photo)
async def send_photo_id(message: types.Message):
    await message.answer(message.photo[-1].file_id)


@router.message(F.text == 'id')
async def send_text_id(message: types.Message):
    await message.answer(str(message.from_user.id))
