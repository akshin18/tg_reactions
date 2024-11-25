from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.accounts.creater import register_account, sign_in
from src.builders.keyboard_button import get_admin_menu
from src.filters.admin_filter import AdminFilter
from src.utils.crud import (
    add_account,
    add_channel,
    delete_account,
    delete_channel,
    get_accounts,
    get_channels,
)
from src.utils.states import AddChannel, CreateAccount, DeleteAccount, DeleteChannel

router = Router()
router.message.filter(AdminFilter())


@router.message(F.text == "Cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Отменено", reply_markup=get_admin_menu())


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
    phone = message.text.replace(" ", "") if message.text else None
    if not phone:
        await message.answer("Номер телефона не введен")
        return
    data["phone"] = phone
    await register_account(phone)
    await state.set_data(data)
    await state.set_state(CreateAccount.code)
    await message.answer("Код из смс:")


@router.message(CreateAccount.code)
async def _(message: Message, state: FSMContext) -> None:
    data = await state.get_data() or {}
    code = message.text.strip() if message.text else None
    if not code:
        await message.answer("Код не введен")
        return
    data["code"] = code
    await state.set_data(data)
    await state.set_state(CreateAccount.pwd)
    await message.answer("Пароль: (если нет, то введите -)")


@router.message(CreateAccount.pwd)
async def _(message: Message, state: FSMContext) -> None:
    data = await state.get_data()

    phone = data.get("phone")
    if not phone:
        await state.clear()
        await message.answer("Ошибка, Номер телефона не найден, попробуйте еще раз")
        return
    code = data.get("code")
    if not code:
        await state.clear()
        await message.answer("Ошибка, Код не найден, попробуйте еще раз")
        return
    password = (
        message.text.strip() if message.text and message.text.strip() != "-" else None
    )
    session_string = await sign_in(phone, code, password)
    if not session_string:
        await state.clear()
        await message.answer("Ошибка Авторизации, попробуйте еще раз")
        return
    await add_account(phone, password, session_string)
    await state.clear()
    await message.answer("Готово!")


@router.message(F.text == "Delete account")
async def delete_account_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(DeleteAccount.phone)
    await message.answer("Введите номер (Пример +799999999):")


@router.message(DeleteAccount.phone)
async def _(message: Message, state: FSMContext) -> None:
    phone = message.text.replace("", "") if message.text else None
    if not phone or not phone.startswith("+"):
        await message.answer("Номер должен начинаться с +")
        return
    result = await delete_account(phone)
    if result:
        await message.answer(f"Удалено {phone}")
    else:
        await message.answer("Такого номера нет в базе")
    await state.clear()


@router.message(F.text == "Get Channels")
async def get_channels_handler(message: Message) -> None:
    await message.answer(await get_channels())


@router.message(F.text == "Add Channel")
async def add_channel_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(AddChannel.channel_id)
    await message.answer("Введите ID канала (Пример: -1009999999):")


@router.message(AddChannel.channel_id)
async def _(message: Message, state: FSMContext) -> None:
    channel_id = message.text.replace(" ", "") if message.text else None
    if not channel_id or not channel_id.startswith("-"):
        await message.answer("ID канала должен начинаться с -")
        return
    await state.set_data({"channel_id": channel_id})
    await state.set_state(AddChannel.channel_link)
    await message.answer("Введите ссылку на канал:")


@router.message(AddChannel.channel_link)
async def _(message: Message, state: FSMContext) -> None:
    channel_link = message.text.replace(" ", "") if message.text else None
    if not channel_link:
        await message.answer("Ссылка на канал не введена")
        return
    data = await state.get_data()
    channel_id = data.get("channel_id")
    if not channel_id:
        await state.clear()
        await message.answer("Ошибка попробуйте заново")
        return

    await add_channel(channel_id, channel_link)
    await state.clear()
    await message.answer("Канал успешно создан")


@router.message(F.text == "Delete Channel")
async def delete_channel_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(DeleteChannel.channel_id)
    await message.answer("Введите ID канала (Пример: -1009999999):")


@router.message(DeleteChannel.channel_id)
async def _(message: Message, state: FSMContext) -> None:
    channel_id = message.text.replace(" ", "") if message.text else None
    if not channel_id or not channel_id.startswith("-"):
        await message.answer("ID канала должен начинаться с -")
        return
    result = await delete_channel(channel_id)
    if result:
        await message.answer(f"Удалено {channel_id}")
    else:
        await message.answer("Такого канала нет в базе")
    await state.clear()


@router.message(Command("start"))
async def activate_handler(message: Message) -> None:
    await default_handler(message)


@router.message()
async def default_handler(message: Message) -> None:
    await message.answer("Main", reply_markup=get_admin_menu())
