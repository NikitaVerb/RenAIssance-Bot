from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def backup_account_inline_kb(backup_account: bool) -> InlineKeyboardMarkup:
    # Создаем inline-клавиатуру с одной кнопкой
    builder = InlineKeyboardBuilder()
    if backup_account:
        builder.button(text="Запросить резервный аккаунт", callback_data="backup_account")
    builder.button(text="↩ Назад в профиль", callback_data="profile")
    builder.adjust(1)
    kb = builder.as_markup()
    return kb
