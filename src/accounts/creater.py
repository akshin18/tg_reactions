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


if __name__ == "__main__":

    async def message_handler(event: NewMessage.Event):
        client: TelegramClient = event.client
        r = await client(
            functions.messages.SendReactionRequest(
                peer=event.message.peer_id,
                msg_id=event.message.id,
                big=True,
                add_to_recent=True,
                reaction=[types.ReactionEmoji(emoticon="👍")],
            )
        )
        print(r)

    from telethon.sessions import StringSession
    from telethon.sync import TelegramClient

    # Replace 'YOUR_STRING_SESSION' with your generated string session
    string_session = "1AZWarzQBuwpse2juTRbzKcxKN2D_k1_uPwfFToY34bLSaUAxO_wh7PhG1i9jVSD-s3ZgS8WYy4sMA6nJqM_0nfU1Z4niBawi0yJjk7Dqqbtm6MFSZo3n_mUm9Od_1CaqemWlEqnAgbfLXCSr4kxA80JjecqHb5i6QE7ZBKvzfR7_2yu6ZQhBf-f3f1tmoYoRf2W4c66LtX8n13iXjO-p56STchrxVqIqLCgIwLwM_BVYylM72FrKl7bIzn8gpDvbacnD5SlTopGP45kThms-5PfWH0K7jbrk0oiiaHvocahdlNWmTjCTa3FUC5hiz6jFf4TgqQsryWagoS9gGaL0pXIM8rw-qP0="
    api_id = 25998004
    api_hash = "4326d6c7ab95948039dcf8d74ed5c29d"

    with TelegramClient(StringSession(string_session), api_id, api_hash) as client:
        print("You are logged in as:", client.get_me().username)
        client.add_event_handler(
            message_handler, event=NewMessage(chats=[-1001899375781])
        )
        client.run_until_disconnected()
