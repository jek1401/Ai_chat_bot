import discord
from discord.ext import commands
import sys
import os
import sqlite3

# --- Путь до корня проекта ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tgbot.config import TOKEN, DB_PATH
from discord_bot.data.database import init_db

# --- Проверка и инициализация базы, если файла нет ---
if not os.path.exists(DB_PATH):
    print(f"📁 База данных не найдена по пути {DB_PATH}, создаю...")
    init_db()
else:
    print(f"✅ База данных найдена: {DB_PATH}")

# --- Интенты ---
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)

# --- Расширения ---
extensions = [
    "bots.commands.auth",
    "bots.commands.help",
    "bots.commands.ai",
    "bots.commands.personalization",
    "bots.commands.points"
]

async def load_extensions():
    for ext in extensions:
        await bot.load_extension(ext)

@bot.event
async def on_ready():
    print(f"✅ Бот запущен как {bot.user}")

async def main():
    await load_extensions()
    await bot.start(TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
