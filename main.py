import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

import config
from handlers import router

logging.basicConfig(level=logging.INFO)

async def main() -> None:
    bot = Bot(token=config.BOT_TOKEN)
    await bot.set_my_commands([
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="cheers", description="Send 🥂")
    ])

    dp = Dispatcher()
    dp.include_router(router)

    logging.info("Bot started.")
    await dp.start_polling(bot)



if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped.")
