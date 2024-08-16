from datetime import datetime

from aiogram import Router
from aiogram import types
from aiogram.filters import Command
from aiogram.types import FSInputFile

import renaissancebot.filters.user_rights
from db import get_all_users, get_user_account

router = Router()
router.message.filter(renaissancebot.filters.user_rights.UserIsAdmin())


# TODO переделать с txt на xls
@router.message(Command('get_users'))
async def get_users(message: types.Message):
    result = await get_all_users()
    file_path = "users_data.txt"  # Имя файла для записи данных

    # Открываем файл для записи
    with open(file_path, 'w', encoding='utf-8') as file:
        for item in result:
            account = await get_user_account(int(item[0])) or '------'
            if item[3] is not None:
                date2 = datetime.strptime(str(item[3]).strip(), '%Y-%m-%d').date()
                sub = 'Действительна' if datetime.now().date() < date2 else 'Недействительна'

                file.write(f'Email: {item[1]}\n'
                           f'Привязан: {account}\n'
                           f'Действие подписки: {item[2]} - {item[3]}\n'
                           f'Статус: {sub}\n'
                           f'Потрачено: {item[4]} руб\n\n')
            else:
                file.write(f'Email: {item[1]}\n'
                           f'Привязан: {account}\n'
                           f'Действие подписки: ------\n'
                           f'Статус: Недействительна\n'
                           f'Потрачено: {item[4]} руб\n\n')

    # Открываем файл для чтения и отправки
    await message.answer_document(FSInputFile('users_data.txt'))
# Отправляем файл пользователю
