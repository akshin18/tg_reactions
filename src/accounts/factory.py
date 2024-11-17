from typing import Dict, Optional

from loguru import logger
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import PhoneCodeExpiredError, PhoneNumberInvalidError
from telethon.sessions import StringSession

from src.config import settings
from src.errors import NotAuthorizedAccountError


class Account:
    def __init__(self, phone: str):
        self.phone = phone
        self.phone_code_hash: str
        self.client: TelegramClient
        self.session_string: str

    async def initialize(self, session_string: str):
        try:
            await self._auth_process(session_string)
        except PhoneNumberInvalidError as e:
            logger.error(e)
            raise e

    async def _auth_process(self, session_string: str):
        await self.create_client(StringSession(session_string))
        is_connected = self.client.is_connected()
        is_authorized = await self.client.is_user_authorized()
        logger.info(f"{is_connected=} {is_authorized=}")
        if not is_authorized:
            raise NotAuthorizedAccountError()
        me = await self.client.get_me()
        logger.info(f"Account {self.phone} authorized {me}")

    async def create_client(self, session: Optional[StringSession] = None) -> None:
        if session is None:
            session = StringSession()
        self.client = TelegramClient(session, settings.API_ID, settings.API_HASH)
        await self.client.connect()
        self.session_string = await self._get_session_string()
        logger.info(f"Client {self.phone} created {self.session_string=}")

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
            await self.client.sign_in(
                phone=self.phone,
                code=code,
                password=password,
                phone_code_hash=self.phone_code_hash,
            )
            self.session_string = await self._get_session_string()
            logger.info(f"New session string: {self.session_string}")
            return True
        except PhoneCodeExpiredError as e:
            logger.error(e)
            return False

    def close(self) -> None:
        self.client.disconnect()

    def __str__(self):
        return f"Client: {self.phone}"


class CreateAccounts:
    accounts: Dict[str, Account] = {}

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


class Workers:
    workers: Dict[str, Account] = {}

    @classmethod
    def add_worker(cls, phone: str) -> Account:
        account = Account(phone)
        cls.workers[phone] = account
        return account

    @classmethod
    def remove_worker(cls, phone: str):
        cls.workers.pop(phone, None)

    @classmethod
    def get_worker(cls, phone: str):
        return cls.workers.get(phone)
