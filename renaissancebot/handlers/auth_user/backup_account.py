from datetime import datetime

from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from db import get_least_linked_backup_account, add_user_backup_account, set_backup_account_date, set_link_date
from keyboards import back_to_profile_inline_kb

router = Router()


@router.callback_query(F.data == "backup_account")
async def backup_account(callback: CallbackQuery, bot: Bot):
    user_id = int(callback.from_user.id)
    backup_account_email = await get_least_linked_backup_account()
    if not backup_account_email:
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                    text="Извините, к сожалению, у нас сейчас нет свободных резервных аккаунтов",
                                    reply_markup=back_to_profile_inline_kb())
        return
    await add_user_backup_account(user_id, backup_account_email)
    await set_backup_account_date(user_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    await set_link_date(user_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                text="Вам выделен резервный аккаунт на один день."
                                     " Посмотреть данные от резервного аккаунта можно в профиле",
                                reply_markup=back_to_profile_inline_kb())
