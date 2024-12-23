import asyncio
import random

from aiogram.client.session.middlewares.request_logging import logger
from telethon import TelegramClient, functions, types
from telethon.events import NewMessage

from src.accounts.factory import Workers
from src.db.models import Accounts, Channels


async def message_handler(event: NewMessage.Event) -> None:
    client: TelegramClient = event.client
    await asyncio.sleep(random.randint(60 * 5, 60 * 50 * 2))


    # Simulate viewing the message
    try:
        logger.info(f"Marking message {event.message.id} as viewed in chat {event.chat_id}")
        await client(
            functions.messages.ReadHistoryRequest(
                peer=event.message.peer_id,
                max_id=event.message.id  # Mark messages up to this ID as read
            )
        )
    except Exception as e:
        logger.error(f"Failed to mark message {event.message.id} as viewed: {e}")


    emoji = random.choice(["👍", "❤️", "🔥", "👏"])
    result = await client(functions.messages.GetAvailableReactionsRequest(hash=0))
    for reaction in result.reactions:
        logger.info(reaction.reaction)
    try:
        await client(
            functions.messages.SendReactionRequest(
                peer=event.message.peer_id,
                msg_id=event.message.id,
                reaction=[types.ReactionEmoji(emoticon=emoji)],
            )
        )
    except Exception as e:
        logger.error(e)
        logger.error(f"error emoji is {emoji}")
    finally:
        logger.info(f"Reacted {event.chat_id}")


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
