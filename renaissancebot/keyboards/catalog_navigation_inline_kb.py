from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def catalog_navigation_inline_kb(total_page: int, page: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    match page:
        case 1:
            kb = [
                [InlineKeyboardButton(text=f"{page}/{total_page}", callback_data="pass"),
                 InlineKeyboardButton(text="➡️", callback_data=f'navigation_{page + 1}')],
                [InlineKeyboardButton(text="1 месяц", callback_data=f'subscribe'),
                 InlineKeyboardButton(text="2 месяца", callback_data=f'subscribe'),
                 InlineKeyboardButton(text="3 месяца", callback_data=f'subscribe')]
            ]
            kb = InlineKeyboardMarkup(inline_keyboard=kb)

        case 2:
            builder.button(text="⬅️", callback_data=f'navigation_{page - 1}')
            builder.button(text=f"{page}/{total_page}", callback_data="pass")
            builder.button(text="Оставить заявку", url='https://t.me/RenAIssanceSupport')
            builder.adjust(2)
            kb = builder.as_markup()
        case _:

            builder.button(text="⬅️", callback_data=f'navigation_{page - 1}')
            builder.button(text=f"{page}/{total_page}", callback_data="pass")
            builder.button(text="➡️", callback_data=f'navigation_{page + 1}')
            builder.button(text="Oформить", callback_data=f'subscribe')
            builder.adjust(3)
            kb = builder.as_markup()

    return kb
