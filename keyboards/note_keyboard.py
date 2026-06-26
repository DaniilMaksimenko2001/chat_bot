from aiogram import types

add_note_button = types.KeyboardButton(text="Добавить заметку")
find_note_button = types.KeyboardButton(text="Найти заметку")
delete_note_button = types.KeyboardButton(text="Удалить заметку")
back_button_from_note_mode = types.KeyboardButton(text="Выход из режима Notes")

note_keyboard = types.ReplyKeyboardMarkup(keyboard=[[add_note_button],
                                                    [find_note_button],
                                                    [delete_note_button],
                                                    [back_button_from_note_mode]],
                                                    resize_keyboard=True)