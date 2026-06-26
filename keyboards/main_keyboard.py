from aiogram import types  
 
ai_mode = types.KeyboardButton(text='AI')  
info_mode = types.KeyboardButton(text='Information')  
task_mode = types.KeyboardButton(text='Notes')  

main_keyboard = types.ReplyKeyboardMarkup(keyboard=[[ai_mode], 
                                                    [info_mode], 
                                                    [task_mode]],
                                                    resize_keyboard=True)