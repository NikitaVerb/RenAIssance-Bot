from aiogram import Router
from aiogram import types
from aiogram.filters import Command

import filters.user_rights

router = Router()
router.message.filter(filters.user_rights.UserIsAdmin())


@router.message(Command('help'))
async def admin_helper(message: types.Message):
    msg = (f"/add_account - добавляет аккаунт ChatGPT+. Добавляет резервный аккаунт, если указать параметр 'r' в конце."
           f"Если вы хотите сделать аккаунт индивидуальным, то добавьте в конце названия почты '_ind'"
           f"\nИспользуйте: /add_account <email>[_ind] <password> [r]\n\n"
           f'/get_data - присылает таблицу xls c информацией о пользователях и аккаунтах, на телефоне может открыть прошлую таблицу с таким названием\n\n'
           f'/get_accounts - присылвает сообщение с аккаунтами ChatGPT+\n\n'
           f'/link - привязывает юзера к аккаунту ChatGPT+ или меняет дату подписки'
           f'\nИспользуйте: /link <account_email> <user_email> [<expiration_date> (ГГГГ-ММ-ДД)]\n\n'
           f'/unlink - отвязывает юзера от аккаунта\nИспользуйте: /unlink <account_email> <user_email>\n\n'
           f'/profile - показывает ваш профиль как пользователя'
           f'/start - запустить бота'
           f'/update_password - заменить пароль от аккаунта ChatGPT+\n'
           f'Используйте: /update_password <account_email> <new_password>\n\n'
           f'/delete_account - удаляет аккаунт из базы данных, если к аккаунту не привязаны пользователи\n'
           f'Используйте: /delete_account <account_email>\n\n'
           f'/add_admin - добавляет админа по его user_id\n'
           f'Используйте: /add_admin <admin_id>"\n\n'
           f'/add_spend - Добавляет деньги к уже потраченным средствам пользователя.\n'
           f'Используйте: /add_spend <user_email> <amount>')
    await message.answer(msg, parse_mode=None)
