import asyncio
import random

from aiogram.client.session.middlewares.request_logging import logger
from telethon import TelegramClient, functions, types
from telethon.events import NewMessage

from src.accounts.factory import Workers
from src.db.models import Accounts, Channels


async def message_handler(event: NewMessage.Event) -> None:
    client: TelegramClient = event.client
    await asyncio.sleep(random.randint(5, 10))
    await client(
        functions.messages.SendReactionRequest(
            peer=event.message.peer_id,
            msg_id=event.message.id,
            big=True,
            add_to_recent=True,
            reaction=[
                types.ReactionEmoji(
                    emoticon=random.choice(["👍", "❤️", "🔥", "👏", "😁"])
                )
            ],
        )
    )
    logger.info("Reacted")


async def main_loop() -> None:
    while True:
        logger.info("start")
        accounts = await Accounts.filter(is_working=True)
        chats = [chat.channel_id for chat in await Channels.all()]
        for account in accounts:
            if account.phone in Workers.workers:
                continue
            worker = Workers.add_worker(account.phone)
            await worker.initialize(account.session_string)
            worker.client.add_event_handler(
                message_handler,
                event=NewMessage(chats=chats),
            )
            asyncio.create_task(worker.client.run_until_disconnected())
            logger.info("Worker Go")
        await asyncio.sleep(5)
