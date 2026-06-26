from aiogram import Router, F
from aiogram.types import Message
from services.ai_service import AIService
from keyboards.main_keyboard import main_keyboard
from keyboards.ai_keyboard import ai_keyboard

ai_service = AIService()

# Храним состояние AI режима для каждого пользователя
ai_mode_enabled = {}

ai_router = Router()

# Вход в AI режим
@ai_router.message(F.text == "AI")
async def ai_mode(message: Message):
    ai_mode_enabled[message.from_user.id] = True
    await message.answer("AI режим включён. Напишите ваш запрос.",reply_markup=ai_keyboard)

# Выход из AI режима по кнопке "Назад"
@ai_router.message(F.text == "Выход из AI режима")
async def exit_ai(message: Message):
    ai_mode_enabled[message.from_user.id] = False
    await message.answer("Вы вышли из AI режима.",reply_markup=main_keyboard)

# Обработка сообщений в AI режиме
@ai_router.message(F.text)
async def handle_ai_message(message: Message):
    user_id = message.from_user.id
    if not ai_mode_enabled.get(user_id, False):
        return
    if message.text.startswith("/"):
        return
    await message.bot.send_chat_action(message.chat.id, "typing") # Включаем в верхней панели "Печатает..."
    response = await ai_service.ask_ai(message.text)
    await message.answer(response)
