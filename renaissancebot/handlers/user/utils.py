from aiogram import Router, F, types

router = Router()


@router.message(F.photo)
async def send_photo_id(message: types.Message):
    await message.answer(message.photo[-1].file_id)
