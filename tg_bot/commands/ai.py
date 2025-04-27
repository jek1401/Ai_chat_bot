from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

import requests
import urllib.parse
import os

from data.database import active_sessions, get_user_data, update_points
from config import VOICE_COST

router = Router()

@router.message(Command("ask"))
async def cmd_ask(message: Message):
    user_id = message.from_user.id
    if user_id not in active_sessions:
        await message.reply("❌ Сначала войдите с /login")
        return
    
    prompt = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None
    if not prompt:
        await message.reply("❌ Введите текст запроса после команды /ask")
        return
    
    user_data = get_user_data(user_id)
    personality = user_data[2] if user_data and user_data[2] else "Hacker"
    
    # Формируем промт с инструкцией для ИИ
    full_prompt = (
        f"Представь, что ты {personality}. "
        f"Ответь на следующее сообщение так, как ответил бы {personality}. "
        f"Сохраняй характер и манеру речи. "
        f"Вот сообщение: {prompt}"
    )
    
    encoded_prompt = urllib.parse.quote(full_prompt)
    url = f"https://text.pollinations.ai/{encoded_prompt}?model=openai-text"

    try:
        response = requests.get(url)
        if response.ok:
            await message.reply(response.text)
        else:
            await message.reply(f"❌ Ошибка: {response.status_code}")
    except Exception as e:
        await message.reply(f"❌ Ошибка: {e}")

@router.message(Command("say"))
async def cmd_say(message: Message):
    user_id = message.from_user.id
    if user_id not in active_sessions:
        await message.reply("❌ Сначала войдите с /login")
        return
    
    prompt = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None
    if not prompt:
        await message.reply("❌ Введите текст запроса после команды /say")
        return
    
    user_data = get_user_data(user_id)
    if not user_data or not user_data[1]:
        await message.reply("❌ Установите голос через /choose")
        return

    voice, points = user_data[1], user_data[0]
    if points < VOICE_COST:
        await message.reply("❌ Недостаточно поинтов. Нужен минимум 5.")
        return

    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://text.pollinations.ai/{encoded_prompt}?model=openai-audio&voice={voice}"

    try:
        response = requests.get(url)
        if response.ok:
            with open("voice.ogg", "wb") as f:
                f.write(response.content)

            # Обновляем поинты в базе данных
            update_points()
            
            await message.reply_voice(voice=open("voice.ogg", "rb"))
            os.remove("voice.ogg")
        else:
            await message.reply("❌ Ошибка при получении аудио.")
    except Exception as e:
        await message.reply(f"❌ Ошибка: {e}")