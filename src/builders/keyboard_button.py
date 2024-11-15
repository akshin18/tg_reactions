from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_admin_menu() -> ReplyKeyboardMarkup:
    buttons = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="First Message"), KeyboardButton(text="Push Message")]
        ],
        resize_keyboard=True,
    )
    return buttons
