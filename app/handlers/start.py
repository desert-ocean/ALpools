from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from app.keyboards.main_menu import get_main_menu

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Добро пожаловать в компанию по строительству бассейнов.\n\n"
        "Выберите интересующий раздел:",
        reply_markup=get_main_menu()
    )