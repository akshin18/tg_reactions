from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.filters.admin_filter import AdminFilter

router = Router()
router.message.filter(AdminFilter())


@router.message(Command("start"))
async def activate_handler(message: Message) -> None:
    await message.answer("Activated!")
