import asyncio
import random

from aiogram.client.session.middlewares.request_logging import logger
from telethon import TelegramClient, functions, types, utils
from telethon.events import NewMessage

from src.accounts.factory import Workers
from src.db.models import Accounts, Channels


async def message_handler(event: NewMessage.Event) -> None:
    client: TelegramClient = event.client
    await asyncio.sleep(random.randint(60 * 5, 60 * 50 * 2))

    # Simulate viewing the message
    try:
        # Fetch the full entity for the peer
        entity = await client.get_entity(event.message.to_id)

        # Convert the entity to an InputPeer
        if isinstance(entity, types.User):
            peer = types.InputPeerUser(entity.id, entity.access_hash)
        elif isinstance(entity, types.Chat):
            peer = types.InputPeerChat(entity.id)
        elif isinstance(entity, types.Channel):
            peer = types.InputPeerChannel(entity.id, entity.access_hash)
        else:
            logger.error(f"Unsupported entity type: {type(entity)}")
            return

        # Mark the message as read
        await client(
            functions.messages.ReadHistoryRequest(peer=peer, max_id=event.message.id)
        )
        logger.info(f"Message {event.message.id} marked as viewed.")

    except Exception as e:
        logger.error(f"Failed to mark message {event.message.id} as viewed: {e}")

    emoji = random.choice(["👍", "❤️", "🔥", "👏"])
    # result = await client(functions.messages.GetAvailableReactionsRequest(hash=0))
    # for reaction in result.reactions:
    #     logger.info(reaction.reaction)
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
