from aiogram import types

back_button_from_ai_mode = types.KeyboardButton(text="Выход из AI режима")
ai_keyboard = types.ReplyKeyboardMarkup(keyboard=[[back_button_from_ai_mode]], resize_keyboard=True)