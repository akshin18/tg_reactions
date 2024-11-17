from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_admin_menu() -> ReplyKeyboardMarkup:
    buttons = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Get Accounts"),
                KeyboardButton(text="Add Account"),
                KeyboardButton(text="Delete accounts"),
            ],
            [
                KeyboardButton(text="Get Channels"),
                KeyboardButton(text="Add Channel"),
                KeyboardButton(text="Delete accounts"),
            ],
            [
                KeyboardButton(text="Statistic"),
            ],
        ],
        resize_keyboard=True,
    )
    return buttons
