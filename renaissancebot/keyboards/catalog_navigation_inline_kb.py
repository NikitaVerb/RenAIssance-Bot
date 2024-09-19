from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def catalog_navigation_inline_kb(total_page: int, page: int) -> InlineKeyboardMarkup:
    match page:
        case 1:
            kb = [
                [InlineKeyboardButton(text=f"{page}/{total_page} стр.", callback_data="pass"),
                 InlineKeyboardButton(text="Далее ➡️", callback_data=f'navigation_{page + 1}')],
                [InlineKeyboardButton(text="Купить 1 месяц — 649 руб", callback_data=f'subscribe_1')],
                [InlineKeyboardButton(text="Купить 3 месяца — 1749 руб", callback_data=f'subscribe_3')],
                [InlineKeyboardButton(text="Купить 6 месяцев — 3349 руб", callback_data=f'subscribe_6')],
                [InlineKeyboardButton(text="↩ Назад в меню", callback_data="menu")]
            ]
            kb = InlineKeyboardMarkup(inline_keyboard=kb)

        case 2:
            kb = [
                [InlineKeyboardButton(text="⬅️ Назад", callback_data=f'navigation_{page - 1}'),
                 InlineKeyboardButton(text=f"{page}/{total_page} стр.", callback_data="pass")],
                [InlineKeyboardButton(text="Купить 1 месяц — 2500 руб", callback_data=f'subscribe_ind')],
                [InlineKeyboardButton(text="↩ Назад в меню", callback_data="menu")]]

            kb = InlineKeyboardMarkup(inline_keyboard=kb)
        case _:
            kb = [
                [InlineKeyboardButton(text="⬅️ назад", callback_data=f'navigation_{page - 1}'),
                 InlineKeyboardButton(text=f"{page}/{total_page}", callback_data="pass"),
                 InlineKeyboardButton(text="далее ➡️", callback_data=f'navigation_{page + 1}')],
                [InlineKeyboardButton(text="Оставить заявку", url='https://t.me/RenAIssanceSupport')],
                [InlineKeyboardButton(text="↩ Назад в меню", callback_data="menu")]]

            kb = InlineKeyboardMarkup(inline_keyboard=kb)
    return kb
