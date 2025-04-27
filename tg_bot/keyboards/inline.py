from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import personalities_list, voices

def auth_keyboard():
    buttons = [
        [InlineKeyboardButton(text="🔑 Вход", callback_data="login")],
        [InlineKeyboardButton(text="📝 Регистрация", callback_data="register")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def personality_keyboard():
    buttons = [
        [InlineKeyboardButton(text=personality, callback_data=f"personality_{personality}")]
        for personality in personalities_list[:5]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def voice_keyboard():
    buttons = [
        [InlineKeyboardButton(text=voice, callback_data=f"voice_{voice}")]
        for voice in voices[:5]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)