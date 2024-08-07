from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def catalog_navigation_inline_kb(total_page: int, page: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    match page:
        case 1:

            builder.button(text=f"{page}/{total_page}", callback_data="pass")
            builder.button(text="➡️", callback_data=f'navigation_{page+1}')
            builder.button(text="Oформить", callback_data=f'subscribe')
            builder.adjust(2)
        case int(total_page):

            builder.button(text="⬅️", callback_data=f'navigation_{page-1}')
            builder.button(text=f"{page}/{total_page}", callback_data="pass")
            builder.button(text="Oформить", callback_data=f'subscribe')
            builder.adjust(2)
        case _:

            builder.button(text="⬅️", callback_data=f'navigation_{page-1}')
            builder.button(text=f"{page}/{total_page}", callback_data="pass")
            builder.button(text="➡️", callback_data=f'navigation_{page+1}')
            builder.button(text="Oформить", callback_data=f'subscribe')
            builder.adjust(3)

    kb = builder.as_markup()
    return kb
