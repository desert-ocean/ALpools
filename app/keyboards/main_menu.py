from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🏊 Индивидуальный расчёт проекта")],
            [KeyboardButton(text="📐 Техническое задание для проектирования")],
            [KeyboardButton(text="🏗 Реализованные проекты")],
            [KeyboardButton(text="🧠 Подбор типа бассейна")],
            [KeyboardButton(text="📞 Консультация ведущего инженера")],
            [KeyboardButton(text="📍 Контакты компании")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите пункт меню",
    )
