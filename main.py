print("=== ЗАПУЩЕН НОВЫЙ MAIN.PY ===")

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from app.config import BOT_TOKEN
from app.handlers.project_configurator import router as project_router
from app.handlers.cost_handler import router as cost_router
from app.handlers.menu import router as menu_router


async def main() -> None:
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    )

    dp = Dispatcher(storage=MemoryStorage())

    # ✅ СНАЧАЛА конфигуратор
    dp.include_router(project_router)

    # ✅ ПОТОМ общее меню (с fallback)
    # ✅ ПОТОМ калькулятор предварительной стоимости
    dp.include_router(cost_router)

    # ✅ В конце общее меню (с fallback)
    dp.include_router(menu_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
