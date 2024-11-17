from typing import Optional

import telethon
from telethon import TelegramClient
from telethon.sessions import StringSession

from src.config import settings


class Account:
    def __init__(self, phone: str, session_string: Optional[str] = None):
        self.phone = phone
        self.phone_code_hash = None
        self.client = None
        self.session_string = None

    async def create_client(self, session: Optional[StringSession] = None) -> None:
        if session is None:
            session = StringSession()
        self.client = TelegramClient(session, settings.API_ID, settings.API_HASH)
        await self.client.connect()
        self.session_string = await self._get_session_string()

    async def _get_session_string(self) -> str:
        return self.client.session.save()

    async def send_otp_code(self) -> None:
        if not self.client:
            await self.create_client()
        sent = await self.client.send_code_request(self.phone)
        self.phone_code_hash = sent.phone_code_hash

    async def sign_in(
        self,
        code: str,
        password: Optional[str] = None,
    ) -> bool:
        try:
            result = await self.client.sign_in(
                phone=self.phone,
                code=code,
                password=password,
                phone_code_hash=self.phone_code_hash,
            )
            print(result)
            return True
        except telethon.errors.rpcerrorlist.PhoneCodeExpiredError as e:
            print("Phone code expired", e)
            return False

    def close(self):
        self.client.disconnect()

    def __str__(self):
        return f"Client: {self.phone}"


class CreateAccounts:
    accounts = {}

    @classmethod
    def add_account(cls, phone: str) -> Account:
        account = Account(phone)
        cls.accounts[phone] = account
        return account

    @classmethod
    def remove_account(cls, phone: str):
        cls.accounts.pop(phone, None)

    @classmethod
    def get_account(cls, phone: str):
        return cls.accounts.get(phone)
