import asyncio
import logging
import os

from google import genai
from google.genai.types import GenerateContentConfig

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, BotCommand
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """
You are an observant AI in a group chat, acting as the ultimate supportive and hyped-up best friend. Your job is to read the user's message and determine if it deserves a toast (🥂). 

You should reply with EXACTLY the word TRUE if the message contains ANY of the following:
1. Deep meaning, profound wisdom, or a highly impactful philosophical sentiment.
2. Strong female empowerment, unapologetic self-love, confidence, or "baddie" energy.
3. Badass, fiercely supportive friend advice, setting boundaries, or cutting off toxic people. The phrase MUST have context and depth.
4. Iconic pop-culture quotes, fun party slogans, or legendary vibes, including transliterated English phrases into Cyrillic.

CRITICAL NEGATIVE CONSTRAINTS (Reply with EXACTLY FALSE if):
- The message is just a single word or a short curse word without context.
- The message lacks actual depth, story, or supportive context. Profanity is allowed ONLY if it is part of a larger, meaningful thought or empowering advice.
- It is just normal mundane chat or boring banter.

If the message truly deserves a toast based on the criteria above, reply with EXACTLY the word: TRUE
Otherwise, reply with EXACTLY the word: FALSE
"""


async def start(message: Message) -> None:
    """Default /start handler with a message"""
    await message.answer("CheersBot activated.")


async def cheers(message: Message) -> None:
    """Manual command to send cheers emoji"""
    await message.answer("🥂")
    try:
        await message.delete()
    except Exception:
        logging.exception("Couldn't delete user's message")


async def analyse_message(message: Message) -> None:
    """Catches every regular text and replies with cheers emoji if it deserves a toast"""
    user_text = message.text

    try:
        response = await client.aio.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_text,
            config=GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT
            )
        )

        ai_decision = response.text.strip().upper()

        if "TRUE" in ai_decision:
            await message.reply("🥂")

    except Exception as e:
        logging.error(f"Gemini API Error: {e}")

async def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN environment is not set.")
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY environment is not set.")

    bot = Bot(token=BOT_TOKEN)
    await bot.set_my_commands([
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="cheers", description="Send 🥂"),
    ])

    dp = Dispatcher()

    dp.message.register(start, Command("start"))
    dp.message.register(cheers, Command("cheers"))

    dp.message.register(analyse_message, F.text & ~F.text.startswith('/'))

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
