from aiogram import Router
from aiogram import types
from aiogram.filters import Command

import renaissancebot.filters.user_rights

router = Router()
router.message.filter(renaissancebot.filters.user_rights.UserIsAdmin())


@router.message(Command('help'))
async def admin_helper(message: types.Message):
    msg = (f'/add_account - добавляет аккаунт ChatGPT+\nИспользуйте: /add_account <email> <password>\n\n'
           f'/get_users - присылает таблицу пользователей xls, на телефоне может открыть прошлую таблицу с таким названием\n\n'
           f'/get_accounts - присылвает сообщение с аккаунтами ChatGPT+\n\n'
           f'/link - привязывает юзера к аккаунту ChatGPT+\nИспользуйте: /link <account_email> <user_email> (<expiration_date>)\n\n'
           f'/unlink - отвязывает юзера от аккаунта\nИспользуйте: /unlink <account_email> <user_email>\n\n'
           f'/profile - показывает ваш профиль как пользователя'
           f'/start - запустить бота'
           f'/update_password - заменить пароль от аккаунта ChatGPT+\n'
           f'Используйте: /update_password <account_email> <new_password>\n\n'
           f'/delete_account - удаляет аккаунт из базы данных, если к аккаунту не привязаны пользователи\n'
           f'Используйте: /delete_account <account_email>\n\n'
           f'/add_admin - добавляет админа по его user_id\n'
           f'Используйте: /add_admin <admin_id>"')
    await message.answer(msg, parse_mode=None)
