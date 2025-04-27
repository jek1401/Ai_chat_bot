from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from data.database import active_sessions, get_user_data
from config import personalities_list, voices
from keyboards.inline import personality_keyboard, voice_keyboard

router = Router()

@router.message(Command("choose"))
async def cmd_choose(message: Message):
    user_id = message.from_user.id
    if user_id not in active_sessions:
        await message.reply("❌ Сначала войдите в аккаунт с /login")
        return
    
    await message.answer(
        "👤 Выберите личность:",
        reply_markup=personality_keyboard()
    )
    
    await message.answer(
        "🎤 Выберите голос:",
        reply_markup=voice_keyboard()
    )

@router.message(Command("personalities"))
async def cmd_personalities(message: Message):
    await message.answer("🎭 Доступные личности:\n" + "\n".join(personalities_list))

@router.message(Command("voices"))
async def cmd_voices(message: Message):
    await message.answer("🎤 Доступные голоса:\n" + "\n".join(voices))

@router.callback_query(F.data.startswith("personality_"))
async def process_personality(callback: CallbackQuery):
    personality = callback.data.split('_', 1)[1]
    user_id = callback.from_user.id
    
    if user_id in active_sessions:
        # Здесь должна быть логика обновления личности в БД
        await callback.message.edit_text(f"✅ Личность установлена: {personality}")
    else:
        await callback.message.edit_text("❌ Сначала войдите в аккаунт")
    
    await callback.answer()

@router.callback_query(F.data.startswith("voice_"))
async def process_voice(callback: CallbackQuery):
    voice = callback.data.split('_', 1)[1]
    user_id = callback.from_user.id
    
    if user_id in active_sessions:
        # Здесь должна быть логика обновления голоса в БД
        await callback.message.edit_text(f"✅ Голос установлен: {voice}")
    else:
        await callback.message.edit_text("❌ Сначала войдите в аккаунт")
    
    await callback.answer()