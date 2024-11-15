import asyncio
import logging

from src.app import bot, dp
from src.handlers.admin import router as admin_router
from src.handlers.client import router as client_router


async def main() -> None:
    dp.include_routers(
        admin_router,
        client_router,
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
