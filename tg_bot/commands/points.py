from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from data.database import active_sessions, get_user_data, update_points

router = Router()

@router.message(Command("points"))
async def cmd_points(message: Message):
    user_id = message.from_user.id
    if user_id not in active_sessions:
        await message.reply("❌ Сначала войдите в аккаунт с /login.")
        return
    
    update_points()
    user_data = get_user_data(user_id)
    
    if user_data:
        await message.reply(f"💰 У вас {user_data[0]} поинтов.")
    else:
        await message.reply("❌ Ошибка при получении данных.")