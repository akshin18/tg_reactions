from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_admin_menu() -> ReplyKeyboardMarkup:
    buttons = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Get Accounts"),
                KeyboardButton(text="Update Account"),
            ],
            [KeyboardButton(text="Statistic"), KeyboardButton(text="Delete accounts")],
        ],
        resize_keyboard=True,
    )
    return buttons
