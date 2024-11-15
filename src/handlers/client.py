from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message()
async def activate_handler(message: Message) -> None:
    await message.answer("Activated! client")
