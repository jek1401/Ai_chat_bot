import os
import logging
import asyncio
from aiogram import Bot, Dispatcher

from config import TOKEN, DB_PATH
from data.database import init_db
from commands import auth, ai, help, personalization, points

# --- Проверка базы данных ---
try:
    if not os.path.exists(DB_PATH):
        print(f"📁 База данных не найдена по пути {DB_PATH}, создаю...")
        init_db()
    else:
        print(f"✅ База данных найдена: {DB_PATH}")
except Exception as e:
    print(f"❌ Ошибка при инициализации базы данных: {e}")
    exit(1)

# --- Логирование ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Регистрация роутеров
    dp.include_router(auth.router)
    dp.include_router(ai.router)
    dp.include_router(help.router)
    dp.include_router(personalization.router)
    dp.include_router(points.router)

    logger.info("Запускаем бота...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())