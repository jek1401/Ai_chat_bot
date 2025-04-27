from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

HELP_TEXT = """
📜 **Команды бота:**

🔐 **Регистрация и вход**
/start — начать работу с ботом  
/login — войти в аккаунт  
/register — зарегистрироваться  

🎭 **Персонализация**
/choose — выбрать личность и голос  
/personalities — список личностей  
/voices — список голосов  

❓ **ИИ**
/ask <сообщение> — текстовая генерация  
/say <сообщение> — голосовая генерация (стоит 5 поинтов)

💰 **Поинты**
/points — баланс поинтов (начисляются каждые 5 мин)

❓ **Помощь**
/help — это сообщение
"""

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(HELP_TEXT)