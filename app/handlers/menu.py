import os
import re
from datetime import datetime

from aiogram import Bot, F, Router
from aiogram.filters import CommandStart
from aiogram.types import (
    FSInputFile,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    User,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from app.config import ADMIN_ID

router = Router()

# ==========================================================
# КНОПКИ МЕНЮ
# ==========================================================

BTN_INDIVIDUAL_CALC = "💰 Предварительная стоимость бассейна"
BTN_TZ = "📥 Скачать техническое задание"
BTN_DESIGN = "📐 Проектирование бассейна"  # ОБРАБАТЫВАЕТСЯ В project_configurator.py
BTN_PROJECTS = "🏗 Реализованные проекты"
BTN_POOL_TYPE = "🧠 Виртуальный конфигуратор"
BTN_CONSULT = "📞 Консультация"
BTN_CONTACTS = "📍 Контакты"

BTN_SEND_PHONE = "📱 Отправить номер"
BTN_BACK = "⬅ Назад в меню"

# ==========================================================
# ПУТИ
# ==========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOCUMENT_PATH = os.path.join(BASE_DIR, "documents", "tz_bass.docx")
COMPANY_CARD_PATH = os.path.join(BASE_DIR, "documents", "rekviz_AKVA_LOGO.DOC")
LEADS_PATH = os.path.join(BASE_DIR, "leads.txt")

PHONE_REGEX = re.compile(r"^\+?[\d\s\-()]{7,20}$")

# ==========================================================
# КЛАВИАТУРЫ
# ==========================================================

def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_INDIVIDUAL_CALC)],
            [KeyboardButton(text=BTN_TZ)],
            [KeyboardButton(text=BTN_DESIGN)],
            [KeyboardButton(text=BTN_PROJECTS)],
            [KeyboardButton(text=BTN_POOL_TYPE)],
            [KeyboardButton(text=BTN_CONSULT)],
            [KeyboardButton(text=BTN_CONTACTS)],
        ],
        resize_keyboard=True,
    )


def get_consultation_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_SEND_PHONE, request_contact=True)],
            [KeyboardButton(text=BTN_BACK)],
        ],
        resize_keyboard=True,
    )

# ==========================================================
# ОБЩИЕ ФУНКЦИИ
# ==========================================================

async def show_main_menu(message: Message, text: str = "Выберите раздел:") -> None:
    await message.answer(text, reply_markup=get_main_menu_keyboard())


async def notify_admin(bot: Bot, user: User, phone: str) -> None:
    created_at = datetime.now().strftime("%d.%m.%Y %H:%M")

    username = f"@{user.username}" if user.username else "не указан"
    full_name = user.full_name or "не указано"

    admin_text = (
        "📞 Новая заявка\n\n"
        f"🕒 Дата: {created_at}\n"
        f"👤 Имя: {full_name}\n"
        f"🔗 Username: {username}\n"
        f"🆔 ID: {user.id}\n"
        f"📱 Телефон: {phone}"
    )

    await bot.send_message(chat_id=ADMIN_ID, text=admin_text)

    with open(LEADS_PATH, "a", encoding="utf-8") as file:
        file.write(admin_text + "\n" + ("-" * 40) + "\n")


async def handle_lead_submission(message: Message, phone: str) -> None:
    await notify_admin(message.bot, message.from_user, phone)

    await message.answer(
        "Спасибо! Наш инженер свяжется с вами в ближайшее время.",
        reply_markup=get_main_menu_keyboard(),
    )

# ==========================================================
# START / НАЗАД
# ==========================================================

@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await show_main_menu(message)


@router.message(F.text == BTN_BACK)
async def back_to_menu(message: Message) -> None:
    await show_main_menu(message)

# ==========================================================
# 📥 СКАЧАТЬ ТЗ
# ==========================================================

@router.message(F.text == BTN_TZ)
async def send_tz_document(message: Message) -> None:

    if os.path.exists(DOCUMENT_PATH):
        await message.answer_document(
            FSInputFile(DOCUMENT_PATH),
            caption=(
                "Техническое задание для проектирования бассейна.\n\n"
                "Передайте архитектору или проектной организации."
            ),
        )
    else:
        await message.answer("Файл временно недоступен.")

    await message.answer(
        "Если требуется индивидуальная версия ТЗ — "
        "оставьте номер телефона для консультации инженера.",
        reply_markup=get_consultation_keyboard(),
    )

# ==========================================================
# 📍 КОНТАКТЫ
# ==========================================================

@router.message(F.text == BTN_CONTACTS)
async def company_contacts(message: Message) -> None:

    text = (
        "ALpools — проектирование и строительство бассейнов\n\n"
        "📍 Москва\n"
        "📞 +7 (495) 644-66-54\n"
        "📧 aanufriev@list.ru\n"
        "🌐 https://www.aqualogo-engineering.ru"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="🌐 Перейти на сайт",
                url="https://www.aqualogo-engineering.ru"
            )],
            [InlineKeyboardButton(
                text="📄 Реквизиты",
                callback_data="send_company_card"
            )],
            [InlineKeyboardButton(
                text="📞 Консультация",
                callback_data="go_consult"
            )],
        ]
    )

    await message.answer(text, reply_markup=keyboard)
    await message.answer_location(latitude=55.669903, longitude=37.552876)


@router.callback_query(F.data == "send_company_card")
async def send_company_card(callback):
    if os.path.exists(COMPANY_CARD_PATH):
        await callback.message.answer_document(FSInputFile(COMPANY_CARD_PATH))
    else:
        await callback.message.answer("Файл временно недоступен.")
    await callback.answer()


@router.callback_query(F.data == "go_consult")
async def go_consult(callback):
    await callback.message.answer(
        "Оставьте номер телефона для консультации инженера.",
        reply_markup=get_consultation_keyboard(),
    )
    await callback.answer()

# ==========================================================
# 📞 КОНСУЛЬТАЦИЯ
# ==========================================================

@router.message(F.text == BTN_CONSULT)
async def request_consultation(message: Message) -> None:
    await message.answer(
        "Оставьте номер телефона для консультации инженера.",
        reply_markup=get_consultation_keyboard(),
    )


@router.message(F.contact)
async def receive_contact(message: Message) -> None:
    if message.contact:
        await handle_lead_submission(message, message.contact.phone_number)


@router.message(F.text.regexp(PHONE_REGEX.pattern))
async def receive_phone_text(message: Message) -> None:
    await handle_lead_submission(message, message.text.strip())

# ==========================================================
# ПРОЧИЕ РАЗДЕЛЫ (без BTN_DESIGN!)
# ==========================================================

@router.message(F.text == BTN_INDIVIDUAL_CALC)
async def individual_calculation(message: Message) -> None:
    await message.answer(
        "Раздел расчёта стоимости находится в разработке."
    )


@router.message(F.text == BTN_PROJECTS)
async def realized_projects(message: Message) -> None:
    await message.answer(
        "Раздел с реализованными проектами скоро будет доступен."
    )


@router.message(F.text == BTN_POOL_TYPE)
async def choose_pool_type(message: Message) -> None:
    await message.answer(
        "Виртуальный конфигуратор находится в разработке."
    )

# ==========================================================
# FALLBACK (ТОЛЬКО ДЛЯ НЕИЗВЕСТНЫХ СООБЩЕНИЙ)
# ==========================================================

@router.message()
async def fallback_handler(message: Message) -> None:
    await message.answer(
        "Пожалуйста, выберите раздел из меню ниже.",
        reply_markup=get_main_menu_keyboard(),
    )