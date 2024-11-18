from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_admin_menu() -> ReplyKeyboardMarkup:
    buttons = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Get Accounts"),
                KeyboardButton(text="Add Account"),
                KeyboardButton(text="Delete account"),
            ],
            [
                KeyboardButton(text="Get Channels"),
                KeyboardButton(text="Add Channel"),
                KeyboardButton(text="Delete Channel"),
            ],
            [
                KeyboardButton(text="Cancel"),
            ],
        ],
        resize_keyboard=True,
    )
    return buttons
