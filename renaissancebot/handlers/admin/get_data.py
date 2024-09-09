import os
from datetime import datetime

import xlwt  # Импортируем библиотеку для работы с Excel
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import FSInputFile

import filters.user_rights
from db import get_all_users, get_user_account, get_user_from_user_backup_account, get_emails_with_user_count, \
    get_inactive_user_count_by_email, get_backup_accounts_with_user_count

router = Router()
router.message.filter(filters.user_rights.UserIsAdmin())


@router.message(Command('get_data'))
async def get_data(message: types.Message):
    all_users = await get_all_users()
    file_path = "data.xls"  # Имя файла для записи данных в формате .xls

    # Создаём новый Excel-файл и рабочий лист
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet("Users Data")
    sheet2 = workbook.add_sheet("Accounts")
    sheet3 = workbook.add_sheet("Backup Accounts")

    # Заголовки столбцов таблицы Backup Accounts
    headers3 = ["Email", "Пароль", "Привязаныые пользователи"]
    for col_num, header in enumerate(headers3):
        sheet3.write(0, col_num, header)

    # Заполняем строки таблицы BackupAccounts
    all_backup_accounts = await get_backup_accounts_with_user_count()
    for row_num, item in enumerate(all_backup_accounts, start=1):
        sheet3.write(row_num, 0, item[0])  # Email
        sheet3.write(row_num, 1, item[1])  # Пароль
        sheet3.write(row_num, 2, item[2])  # Привязанные пользователи

    # Заголовки столбцов таблицы Users Data
    headers1 = ['Email', 'Привязан', 'Дата покупки', 'Дата окончания', 'Статус',
                'Резервный аккаунт', 'Выдача резервного аккаунта', 'Потрачено']
    for col_num, header in enumerate(headers1):
        sheet.write(0, col_num, header)

    # Заголовки столбцов таблицы Accounts
    headers2 = ['Email', 'Пароль', 'Привязанные пользоватлей', 'Недейств. пользователи']
    for col_num, header in enumerate(headers2):
        sheet2.write(0, col_num, header)
    # Заполняем строки таблицы Accounts данными
    all_accounts = await get_emails_with_user_count()
    for row_num, item in enumerate(all_accounts, start=1):
        sheet2.write(row_num, 0, item[0])  # Email
        sheet2.write(row_num, 1, item[1])  # Пароль
        sheet2.write(row_num, 2, item[2])  # Привязанные пользователи
        sheet2.write(row_num, 3, await get_inactive_user_count_by_email(item[0]))  # Недействю пользователи

    # Заполняем строки таблицы Users Data данными пользователей
    for row_num, item in enumerate(all_users, start=1):
        user_id = int(item[0])
        account = await get_user_account(user_id)
        user_from_user_backup_accounts = await get_user_from_user_backup_account(user_id)
        if user_from_user_backup_accounts:
            user_backup_account = str(user_from_user_backup_accounts[1])
            link_date = str(user_from_user_backup_accounts[2])
        else:
            user_backup_account = None
            link_date = None
        if item[3] is not None:
            date2 = datetime.strptime(str(item[3]).strip(), '%Y-%m-%d').date()
            sub = 'Действительна' if datetime.now().date() < date2 else 'Недействительна'

        else:
            sub = 'Недействительна'

        sheet.write(row_num, 0, item[1])  # Email
        sheet.write(row_num, 1, account)  # Привязан
        sheet.write(row_num, 2, item[2])  # Дата покупки
        sheet.write(row_num, 3, item[3])  # Дата окончания
        sheet.write(row_num, 4, sub)  # Статус
        sheet.write(row_num, 5, user_backup_account)  # Резервный аккаунт
        sheet.write(row_num, 6, link_date)  # Выдача резервного аккаунта
        sheet.write(row_num, 7, item[4])  # Потрачено

    # Сохраняем Excel-файл
    workbook.save(file_path)

    # Отправляем файл пользователю
    await message.answer_document(FSInputFile(file_path))

    # Удаляем файл после отправки
    os.remove(file_path)
