from aiogram.fsm.state import State, StatesGroup


class CreateAccount(StatesGroup):
    phone = State()
    code = State()
    pwd = State()
