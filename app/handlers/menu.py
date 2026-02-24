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

BTN_INDIVIDUAL_CALC = "🏊 Индивидуальный расчёт проекта"
BTN_TZ = "📐 Техническое задание для проектирования"
BTN_PROJECTS = "🏗 Реализованные проекты"
BTN_POOL_TYPE = "🧠 Подбор типа бассейна"
BTN_CONSULT = "📞 Консультация ведущего инженера"
BTN_CONTACTS = "📍 Контакты компании"

BTN_SEND_PHONE = "📱 Отправить номер"
BTN_BACK = "⬅ Назад в меню"

# ==========================================================
# ПУТИ
# ==========================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

DOCUMENT_PATH = os.path.join(PROJECT_ROOT, "documents", "tz_bass.docx")
COMPANY_CARD_PATH = os.path.join(PROJECT_ROOT, "documents", "rekviz_AKVA_LOGO.DOC")
LEADS_PATH = os.path.join(PROJECT_ROOT, "leads.txt")

# ==========================================================

PHONE_REGEX = re.compile(r"^\+?[\d\s\-()]{7,20}$")


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_INDIVIDUAL_CALC)],
            [KeyboardButton(text=BTN_TZ)],
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


async def show_main_menu(message: Message, text: str = "Выберите действие из меню:") -> None:
    await message.answer(text, reply_markup=get_main_menu_keyboard())


async def notify_admin(bot: Bot, user: User, phone: str) -> None:
    created_at = datetime.now().strftime("%d.%m.%Y %H:%M")
    username = user.username if user.username else "не указан"
    full_name = user.full_name if user.full_name else "не указано"

    admin_text = (
        "📞 Новая заявка на консультацию\n\n"
        f"🕒 Дата: {created_at}\n"
        f"👤 Имя: {full_name}\n"
        f"🔗 Username: {username}\n"
        f"🆔 ID: {user.id}\n"
        f"📱 Телефон: {phone}"
    )

    await bot.send_message(chat_id=ADMIN_ID, text=admin_text)

    with open(LEADS_PATH, "a", encoding="utf-8") as leads_file:
        leads_file.write(admin_text + "\n" + ("-" * 40) + "\n")


async def handle_lead_submission(message: Message, phone: str) -> None:
    await notify_admin(bot=message.bot, user=message.from_user, phone=phone)
    await show_main_menu(
        message,
        text="Спасибо! Ведущий инженер свяжется с вами.",
    )


# ==========================================================
# ОБРАБОТЧИКИ
# ==========================================================

@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await show_main_menu(message)


@router.message(F.text == BTN_BACK)
async def back_to_menu(message: Message) -> None:
    await show_main_menu(message)


@router.message(F.text == BTN_TZ)
async def send_tz_document(message: Message) -> None:
    if os.path.exists(DOCUMENT_PATH):
        document = FSInputFile(DOCUMENT_PATH)
        await message.answer_document(
            document=document,
            caption=(
                "Направляем техническое задание для проектирования бассейна.\n\n"
                "Документ рекомендуется передать архитектору или проектной группе."
            ),
        )
    else:
        await message.answer(
            "Файл технического задания временно недоступен. "
            "Пожалуйста, свяжитесь с нами для получения документа.",
        )

    await message.answer(
        "При необходимости подготовим индивидуальную версию ТЗ\n"
        "с учётом особенностей вашего объекта.\n\n"
        "Оставьте номер телефона для консультации инженера.",
        reply_markup=get_consultation_keyboard(),
    )


# ==========================================================
# КОНТАКТЫ КОМПАНИИ
# ==========================================================

@router.message(F.text == BTN_CONTACTS)
async def company_contacts(message: Message) -> None:
    contacts_text = (
        "📍 ALpools — проектирование и строительство бассейнов\n\n"
        "🏢 Частные и коммерческие объекты\n"
        "📍 Москва\n\n"
        "📞 +7 (495) 644-66-54\n"
        "📧 aanufriev@list.ru\n"
        "🌐 https://www.aqualogo-engineering.ru\n\n"
        "📍 Адрес:\n"
        "г. Москва, ул. Профсоюзная, д. 57\n\n"
        "⏰ Пн–Пт: 09:00–18:00\n"
        "Сб–Вс: по согласованию"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📞 Показать номер",
                    callback_data="show_phone"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🌐 Перейти на сайт",
                    url="https://www.aqualogo-engineering.ru"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📄 Реквизиты компании",
                    callback_data="send_company_card"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📞 Консультация инженера",
                    callback_data="go_consult"
                )
            ],
        ]
    )

    await message.answer(contacts_text, reply_markup=keyboard)

    await message.answer_location(
        latitude=55.669903,
        longitude=37.552876
    )


@router.callback_query(F.data == "show_phone")
async def show_phone(callback):
    await callback.message.answer(
        "📞 Телефон компании:\n\n"
        "+7 (495) 644-66-54\n\n"
        "Вы можете нажать на номер и позвонить."
    )
    await callback.answer()


@router.callback_query(F.data == "send_company_card")
async def send_company_card(callback):
    if os.path.exists(COMPANY_CARD_PATH):
        document = FSInputFile(COMPANY_CARD_PATH)
        await callback.message.answer_document(document)
    else:
        await callback.message.answer("Файл с реквизитами временно недоступен.")
    await callback.answer()


@router.callback_query(F.data == "go_consult")
async def go_consult(callback):
    await callback.message.answer(
        "Оставьте номер телефона для консультации инженера.",
        reply_markup=get_consultation_keyboard(),
    )
    await callback.answer()


# ==========================================================
# КОНСУЛЬТАЦИЯ
# ==========================================================

@router.message(F.text == BTN_CONSULT)
async def request_consultation(message: Message) -> None:
    await message.answer(
        "Оставьте номер телефона для консультации инженера.",
        reply_markup=get_consultation_keyboard(),
    )


@router.message(F.contact)
async def receive_contact(message: Message) -> None:
    if message.contact and message.contact.phone_number:
        await handle_lead_submission(message, phone=message.contact.phone_number)


@router.message(F.text.regexp(PHONE_REGEX.pattern))
async def receive_phone_text(message: Message) -> None:
    if message.text:
        await handle_lead_submission(message, phone=message.text.strip())


# ==========================================================
# ПРОЧИЕ РАЗДЕЛЫ
# ==========================================================

@router.message(F.text == BTN_INDIVIDUAL_CALC)
async def individual_calculation(message: Message) -> None:
    await message.answer(
        "Раздел индивидуального расчёта проекта в разработке. "
        "Оставьте номер в разделе консультации, и инженер свяжется с вами.",
    )


@router.message(F.text == BTN_PROJECTS)
async def realized_projects(message: Message) -> None:
    await message.answer("Раздел с реализованными проектами скоро будет доступен.")


@router.message(F.text == BTN_POOL_TYPE)
async def choose_pool_type(message: Message) -> None:
    await message.answer("Подбор типа бассейна скоро будет доступен.")


@router.message()
async def fallback_handler(message: Message) -> None:
    await show_main_menu(message)