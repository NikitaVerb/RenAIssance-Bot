from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def catalog_navigation_inline_kb(total_page: int, page: int) -> InlineKeyboardMarkup:
    match page:
        case 1:
            kb = [
                [InlineKeyboardButton(text=f"{page}/{total_page}", callback_data="pass"),
                 InlineKeyboardButton(text="➡️", callback_data=f'navigation_{page + 1}')],
                [InlineKeyboardButton(text="1 месяц", callback_data=f'subscribe_1'),
                 InlineKeyboardButton(text="3 месяца", callback_data=f'subscribe_3'),
                 InlineKeyboardButton(text="6 месяца", callback_data=f'subscribe_6')],
                [InlineKeyboardButton(text="↩Назад в меню", callback_data="menu")]
            ]
            kb = InlineKeyboardMarkup(inline_keyboard=kb)

        case 2:
            kb = [
                [InlineKeyboardButton(text="⬅️", callback_data=f'navigation_{page - 1}'),
                 InlineKeyboardButton(text=f"{page}/{total_page}", callback_data="pass")],
                [InlineKeyboardButton(text="Оставить заявку", url='https://t.me/RenAIssanceSupport')],
                [InlineKeyboardButton(text="↩Назад в меню", callback_data="menu")]]

            kb = InlineKeyboardMarkup(inline_keyboard=kb)
        case _:
            kb = [
                [InlineKeyboardButton(text="⬅️", callback_data=f'navigation_{page - 1}'),
                 InlineKeyboardButton(text=f"{page}/{total_page}", callback_data="pass"),
                 InlineKeyboardButton(text="➡️", callback_data=f'navigation_{page + 1}')],
                [InlineKeyboardButton(text="Оставить заявку", url='https://t.me/RenAIssanceSupport')],
                [InlineKeyboardButton(text="↩Назад в меню", callback_data="menu")]]

            kb = InlineKeyboardMarkup(inline_keyboard=kb)
    return kb
