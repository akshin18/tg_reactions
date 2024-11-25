from aiogram.fsm.state import State, StatesGroup


class CreateAccount(StatesGroup):
    phone = State()
    code = State()
    pwd = State()


class DeleteAccount(StatesGroup):
    phone = State()


class AddChannel(StatesGroup):
    channel_id = State()
    channel_link = State()


class DeleteChannel(StatesGroup):
    channel_id = State()
