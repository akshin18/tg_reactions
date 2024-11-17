from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.accounts.creater import register_account, sign_in
from src.builders.keyboard_button import get_admin_menu
from src.filters.admin_filter import AdminFilter
from src.utils.crud import add_account, get_accounts
from src.utils.states import CreateAccount

router = Router()
router.message.filter(AdminFilter())


@router.message(F.text == "Get Accounts")
async def get_accounts_handler(message: Message) -> None:
    accounts = await get_accounts()
    await message.answer(accounts)


@router.message(F.text == "Add Account")
async def add_account_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(CreateAccount.phone)
    await message.answer("Номер Телефона: (Пример: +79999999999)")


@router.message(CreateAccount.phone)
async def _(message: Message, state: FSMContext) -> None:
    data = await state.get_data() or {}
    phone = message.text.replace(" ", "")
    data["phone"] = phone
    await register_account(phone)
    await state.set_data(data)
    await state.set_state(CreateAccount.code)
    await message.answer("Код из смс:")


@router.message(CreateAccount.code)
async def _(message: Message, state: FSMContext) -> None:
    data = await state.get_data() or {}
    data["code"] = message.text.strip()
    await state.set_data(data)
    await state.set_state(CreateAccount.pwd)
    await message.answer("Пароль: (если нет, то введите -)")


@router.message(CreateAccount.pwd)
async def _(message: Message, state: FSMContext) -> None:
    data = await state.get_data()

    phone = data.get("phone")
    code = data.get("code")
    password = message.text.strip() if message.text.strip() != "-" else None
    session_string = await sign_in(phone, code, password)
    if not session_string:
        await state.clear()
        await message.answer("Ошибка Авторизации, попробуйте еще раз")
        return
    await add_account(phone, password, session_string)
    await state.clear()
    await message.answer("Готово!")


@router.message(Command("start"))
async def activate_handler(message: Message) -> None:
    await default_handler(message)


@router.message()
async def default_handler(message: Message) -> None:
    await message.answer("Main", reply_markup=get_admin_menu())
