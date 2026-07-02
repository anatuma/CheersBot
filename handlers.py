import logging

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import Message

from ai_service import evaluate_for_toast

router = Router()

@router.message(Command("start"))
async def start(message: Message) -> None:
    """Default /start handler"""
    await message.answer("CheersBot activated.")

@router.message(Command("cheers"))
async def cheers(message: Message) -> None:
    """Manual command to send cheers emoji"""
    await message.answer("🥂")
    try:
        await message.delete()
    except TelegramBadRequest:
        logging.warning(f"Lacked permission to delete message in chat {message.chat.id}")
    except Exception as e:
        logging.error(f"Unexpected error deleting message: {e}")

@router.message(F.text & ~F.text.startswith('/'))
async def analyse_message(message: Message) -> None:
    """Catches every regular text and evaluates it using AI."""
    deserves_toast = await evaluate_for_toast(message.text)
    if deserves_toast:
        await message.reply("🥂")