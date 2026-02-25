from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from app.config import ADMIN_ID
from app.handlers.menu import BTN_DESIGN

router = Router()

# =====================================================
# НАСТРОЙКИ ПРОЕКТА
# =====================================================

PROJECT_SECTIONS = {
    "technology": {"name": "Технология", "price": 120_000, "option_percent": 15},
    "architecture": {"name": "Архитектура", "price": 90_000, "option_percent": 10},
    "electric": {"name": "Электрика", "price": 80_000, "option_percent": 12},
    "automation": {"name": "Автоматизация", "price": 70_000, "option_percent": 15},
    "constructive": {"name": "Конструктив", "price": 100_000, "option_percent": 8},
}

ATTRACTION_PRICE = 25_000

TYPE_COEFFICIENT = {
    "private": 1.0,
    "public": 1.4,
}

PLACEMENT_COEFFICIENT = {
    "indoor": 1.2,
    "outdoor": 1.0,
}

# =====================================================
# FSM
# =====================================================

class ProjectFSM(StatesGroup):
    choosing_sections = State()
    choosing_type = State()
    choosing_placement = State()
    choosing_attractions = State()
    result = State()
    waiting_phone = State()
    waiting_email = State()


# =====================================================
# КЛАВИАТУРЫ
# =====================================================

def sections_keyboard(selected: list[str]) -> InlineKeyboardMarkup:
    buttons = []

    for key, section in PROJECT_SECTIONS.items():
        mark = "☑" if key in selected else "⬜"
        buttons.append([
            InlineKeyboardButton(
                text=f"{mark} {section['name']} ({section['price']:,} ₽)",
                callback_data=f"section:{key}",
            )
        ])

    buttons.append([
        InlineKeyboardButton(text="➡ Продолжить", callback_data="sections:next")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def attractions_keyboard(current: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="➖", callback_data="attr:minus"),
            InlineKeyboardButton(text=str(current), callback_data="attr:noop"),
            InlineKeyboardButton(text="➕", callback_data="attr:plus"),
        ],
        [
            InlineKeyboardButton(text="💰 Рассчитать", callback_data="attr:calculate")
        ],
    ])


# =====================================================
# СТАРТ
# =====================================================

@router.message(F.text == BTN_DESIGN)
async def start_configurator(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(ProjectFSM.choosing_sections)
    await state.update_data(sections=[], attractions=0)

    await message.answer(
        "📐 <b>Выберите разделы проектирования:</b>",
        reply_markup=sections_keyboard([]),
    )


# =====================================================
# ВЫБОР РАЗДЕЛОВ
# =====================================================

@router.callback_query(ProjectFSM.choosing_sections, F.data.startswith("section:"))
async def toggle_section(callback: CallbackQuery, state: FSMContext):
    key = callback.data.split(":")[1]

    data = await state.get_data()
    selected = data.get("sections", [])

    if key in selected:
        selected.remove(key)
    else:
        selected.append(key)

    await state.update_data(sections=selected)

    await callback.message.edit_reply_markup(
        reply_markup=sections_keyboard(selected)
    )

    await callback.answer()


@router.callback_query(ProjectFSM.choosing_sections, F.data == "sections:next")
async def go_to_type(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if not data.get("sections"):
        await callback.answer("Выберите хотя бы один раздел", show_alert=True)
        return

    await state.set_state(ProjectFSM.choosing_type)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Частный", callback_data="type:private"),
            InlineKeyboardButton(text="Общественный", callback_data="type:public"),
        ]
    ])

    await callback.message.answer(
        "🏊 <b>Выберите тип бассейна:</b>",
        reply_markup=keyboard,
    )

    await callback.answer()


# =====================================================
# ТИП БАССЕЙНА
# =====================================================

@router.callback_query(ProjectFSM.choosing_type, F.data.startswith("type:"))
async def choose_pool_type(callback: CallbackQuery, state: FSMContext):
    pool_type = callback.data.split(":")[1]

    await state.update_data(pool_type=pool_type)
    await state.set_state(ProjectFSM.choosing_placement)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Внутри здания", callback_data="place:indoor"),
            InlineKeyboardButton(text="Отдельно стоящий", callback_data="place:outdoor"),
        ]
    ])

    await callback.message.answer(
        "📍 <b>Размещение бассейна:</b>",
        reply_markup=keyboard,
    )

    await callback.answer()


# =====================================================
# РАЗМЕЩЕНИЕ
# =====================================================

@router.callback_query(ProjectFSM.choosing_placement, F.data.startswith("place:"))
async def choose_placement(callback: CallbackQuery, state: FSMContext):
    placement = callback.data.split(":")[1]

    await state.update_data(placement=placement, attractions=0)
    await state.set_state(ProjectFSM.choosing_attractions)

    await callback.message.answer(
        "🎢 <b>Выберите количество аттракционов (до 5):</b>",
        reply_markup=attractions_keyboard(0),
    )

    await callback.answer()


# =====================================================
# АТТРАКЦИОНЫ
# =====================================================

@router.callback_query(ProjectFSM.choosing_attractions, F.data.startswith("attr:"))
async def manage_attractions(callback: CallbackQuery, state: FSMContext):
    action = callback.data.split(":")[1]
    data = await state.get_data()
    count = data.get("attractions", 0)

    if action == "plus" and count < 5:
        count += 1
    elif action == "minus" and count > 0:
        count -= 1
    elif action == "calculate":
        await calculate_price(callback, state)
        return

    await state.update_data(attractions=count)

    await callback.message.edit_reply_markup(
        reply_markup=attractions_keyboard(count)
    )

    await callback.answer()


# =====================================================
# РАСЧЁТ
# =====================================================

async def calculate_price(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    sections = data.get("sections", [])
    pool_type = data.get("pool_type")
    placement = data.get("placement")
    attractions = data.get("attractions", 0)

    total = 0
    breakdown = ["📐 <b>Выбранные разделы:</b>\n"]

    for key in sections:
        section = PROJECT_SECTIONS[key]
        base = section["price"]
        extra = base * section["option_percent"] / 100
        section_total = base + extra
        total += section_total

        breakdown.append(
            f"• <b>{section['name']}</b>\n"
            f"   Базовая: {base:,} ₽\n"
            f"   Доп. ({section['option_percent']}%): {int(extra):,} ₽\n"
            f"   Итого: {int(section_total):,} ₽\n"
        )

    attractions_sum = attractions * ATTRACTION_PRICE
    total += attractions_sum

    if attractions:
        breakdown.append(
            f"\n🎢 Аттракционы: {attractions} × {ATTRACTION_PRICE:,} ₽ = {attractions_sum:,} ₽"
        )

    total = int(total * TYPE_COEFFICIENT[pool_type] * PLACEMENT_COEFFICIENT[placement])

    await state.update_data(total=total)
    await state.set_state(ProjectFSM.result)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📨 Отправить заявку", callback_data="send")]
    ])

    await callback.message.answer(
        "💰 <b>Предварительный расчёт</b>\n\n"
        + "\n".join(breakdown)
        + "\n\n━━━━━━━━━━━━━━━\n"
        + f"<b>ИТОГО: {total:,} ₽</b>\n\n"
        + "⚠ <i>Расчёт ориентировочный.</i>",
        reply_markup=keyboard,
    )

    await callback.answer()


# =====================================================
# ЗАПРОС КОНТАКТОВ
# =====================================================

@router.callback_query(ProjectFSM.result, F.data == "send")
async def request_phone(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ProjectFSM.waiting_phone)

    await callback.message.answer(
        "📱 <b>Введите ваш номер телефона:</b>\n"
        "Например: +7 999 123 45 67"
    )

    await callback.answer()


@router.message(ProjectFSM.waiting_phone)
async def process_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text.strip())
    await state.set_state(ProjectFSM.waiting_email)

    await message.answer(
        "📧 <b>Введите email (или напишите - если не хотите указывать):</b>"
    )


@router.message(ProjectFSM.waiting_email)
async def process_email(message: Message, state: FSMContext):
    email = message.text.strip()
    if email == "-":
        email = "Не указан"

    await state.update_data(email=email)
    data = await state.get_data()

    user = message.from_user

    sections_list = "\n".join(
        f"• {PROJECT_SECTIONS[s]['name']}" for s in data.get("sections", [])
    )

    admin_text = (
        "📥 <b>НОВАЯ ЗАЯВКА</b>\n\n"
        f"👤 {user.full_name}\n"
        f"🆔 {user.id}\n"
        f"📱 {data.get('phone')}\n"
        f"📧 {data.get('email')}\n\n"
        f"📐 Разделы:\n{sections_list}\n\n"
        f"💰 Сумма: <b>{data.get('total', 0):,} ₽</b>"
    )

    await message.bot.send_message(ADMIN_ID, admin_text)

    await message.answer(
        "✅ Заявка отправлена.\nНаш специалист свяжется с вами."
    )

    await state.clear()