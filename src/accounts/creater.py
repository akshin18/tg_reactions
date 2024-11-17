from typing import Optional

from telethon import functions, types
from telethon.events import NewMessage

from src.accounts.factory import Account, CreateAccounts
from src.errors import NoClientError


async def register_account(phone: str) -> None:
    account = CreateAccounts.add_account(phone)
    await account.send_otp_code()


async def get_account(phone: str) -> Account:
    account = CreateAccounts.get_account(phone)
    if not account:
        raise NoClientError()
    return account


async def remove_account(phone: str) -> None:
    CreateAccounts.remove_account(phone)


async def sign_in(phone: str, code: str, password: str) -> Optional[str]:
    account = await get_account(phone)
    result = await account.sign_in(code, password)
    if not result:
        return
    return account.session_string
