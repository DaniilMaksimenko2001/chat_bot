from aiogram import types

weather_button = types.KeyboardButton(text="Погода")
exchange_rate_button = types.KeyboardButton(text="Курсы валют")
back_button_from_info_mode = types.KeyboardButton(text="Выход из модуля Information")
info_keyboard = types.ReplyKeyboardMarkup(keyboard=[[weather_button],
                                                    [exchange_rate_button],
                                                    [back_button_from_info_mode]], 
                                                    resize_keyboard=True)