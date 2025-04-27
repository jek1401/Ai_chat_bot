from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from data.database import active_sessions, register_user, login_user
from keyboards.inline import auth_keyboard

router = Router()

class AuthStates(StatesGroup):
    waiting_for_login = State()
    waiting_for_register = State()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "🔐 Добро пожаловать! Выберите действие:",
        reply_markup=auth_keyboard()
    )

@router.callback_query(F.data == "login")
async def process_login(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("👋 Введите имя пользователя и пароль в формате: имя пароль")
    await state.set_state(AuthStates.waiting_for_login)
    await callback.answer()

@router.callback_query(F.data == "register")
async def process_register(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("👋 Введите имя пользователя и пароль для регистрации в формате: имя пароль")
    await state.set_state(AuthStates.waiting_for_register)
    await callback.answer()

@router.message(AuthStates.waiting_for_login)
async def process_login_credentials(message: Message, state: FSMContext):
    user_input = message.text.split(maxsplit=1)
    if len(user_input) != 2:
        await message.reply("❌ Неверный формат. Введите: имя пароль")
        return
    
    username, password = user_input
    if login_user(message.from_user.id, username, password):
        await message.reply(f"🔐 Вход выполнен как {username}")
    else:
        await message.reply("❌ Неверные данные для входа.")
    
    await state.clear()

@router.message(AuthStates.waiting_for_register)
async def process_register_credentials(message: Message, state: FSMContext):
    user_input = message.text.split(maxsplit=1)
    if len(user_input) != 2:
        await message.reply("❌ Неверный формат. Введите: имя пароль")
        return
    
    username, password = user_input
    success, result = register_user(username, password)
    await message.reply(result)
    
    if success:
        login_user(message.from_user.id, username, password)
    
    await state.clear()