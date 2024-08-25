import os
from datetime import datetime

import xlwt  # Импортируем библиотеку для работы с Excel
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import FSInputFile

import renaissancebot.filters.user_rights
from db import get_all_users, get_user_account

router = Router()
router.message.filter(renaissancebot.filters.user_rights.UserIsAdmin())


@router.message(Command('get_users'))
async def get_users(message: types.Message):
    result = await get_all_users()
    file_path = "users_data.xls"  # Имя файла для записи данных в формате .xls

    # Создаём новый Excel-файл и рабочий лист
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet("Users Data")

    # Заголовки столбцов
    headers = ['Email', 'Привязан', 'Дата покупки', 'Дата окончания', 'Статус', 'Потрачено']
    for col_num, header in enumerate(headers):
        sheet.write(0, col_num, header)

    # Заполняем строки данными пользователей
    for row_num, item in enumerate(result, start=1):
        account = await get_user_account(int(item[0])) or '------'
        if item[3] is not None:
            date2 = datetime.strptime(str(item[3]).strip(), '%Y-%m-%d').date()
            sub = 'Действительна' if datetime.now().date() < date2 else 'Недействительна'

        else:
            sub = 'Недействительна'

        sheet.write(row_num, 0, item[1])  # Email
        sheet.write(row_num, 1, account)  # Привязан
        sheet.write(row_num, 2, item[2] or '-------')  # Дата покупки
        sheet.write(row_num, 3, item[3] or '-------')  # Дата продажи
        sheet.write(row_num, 4, sub)  # Статус
        sheet.write(row_num, 5, item[4])  # Потрачено

    # Сохраняем Excel-файл
    workbook.save(file_path)

    # Отправляем файл пользователю
    await message.answer_document(FSInputFile(file_path))

    # Удаляем файл после отправки
    os.remove(file_path)
