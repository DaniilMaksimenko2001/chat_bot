from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from datetime import datetime
from keyboards.note_keyboard import note_keyboard
from keyboards.main_keyboard import main_keyboard

class Note:
    def __init__(self, text: str, date: str, time: str):
        self.text = text
        self.date = date  
        self.time = time

class NoteService:
    def __init__(self):
        self.notes = {}  # {user_id: [Note, Note]}
    def add_note(self, user_id: int, note: Note):
        self.notes.setdefault(user_id, []).append(note)
    def get_notes(self, user_id: int):
        return self.notes.get(user_id, [])
    def find_by_date(self, user_id: int, date: str):
        return [n for n in self.notes.get(user_id, []) if n.date == date]
    def delete_note(self, user_id: int, index: int):
        if user_id in self.notes and 0 <= index < len(self.notes[user_id]):
            self.notes[user_id].pop(index)
            return True
        return False
    
note_service = NoteService()

class NoteState(StatesGroup):
    waiting_for_note = State()
    waiting_for_search_date = State()
    waiting_for_delete_index = State()

note_router = Router()

@note_router.message(F.text == "Notes")
async def notes_mode(message: Message):
    await message.answer("📝 Режим заметок", reply_markup=note_keyboard)

@note_router.message(F.text == "Выход из режима Notes")
async def back_to_main_menu(message: Message):
    await message.answer("Главное меню", reply_markup=main_keyboard)

# Добавление заметки
@note_router.message(F.text == "Добавить заметку")
async def add_note(message: Message, state: FSMContext):
    await state.set_state(NoteState.waiting_for_note)
    await message.answer("✏️ Напиши текст заметки:")

@note_router.message(NoteState.waiting_for_note)
async def process_note_text(message: Message, state: FSMContext):
    user_id = message.from_user.id
    now = datetime.now()
    date = now.strftime("%d.%m.%Y") # String Format Time - форматирование даты в строку
    time = now.strftime("%H:%M")
    note = Note(message.text, date, time)
    note_service.add_note(user_id, note)
    await message.answer(
        f"✅ Заметка добавлена:\n"
        f"{message.text}\n"
        f"📅 Дата: {date}\n"
        f"⏰ Время: {time}"
    )
    await state.clear()

# Поиск по дате
@note_router.message(F.text == "Найти заметку")
async def find_note(message: Message, state: FSMContext):
    await state.set_state(NoteState.waiting_for_search_date)
    await message.answer("🔍 Введите дату в формате DD.MM.YYYY.\n")

@note_router.message(NoteState.waiting_for_search_date)
async def process_find(message: Message, state: FSMContext):
    user_id = message.from_user.id
    date = message.text.strip()
    try:
        datetime.strptime(date, "%d.%m.%Y") # String Parse Time - парсинг/анализ строки во время
    except ValueError:
        await message.answer("❌ Неверный формат. Используйте DD.MM.YYYY")
        return
    results = note_service.find_by_date(user_id, date)
    if not results:
        await message.answer("📭 Заметок за эту дату нет")
    else:
        text = f"📅 Заметки за {date}:\n\n"
        for i, note in enumerate(results, start=1): # Возвращаем кортежи (номер, элемент)
            text += f"{i}. {note.text}\n⏰ {note.time}\n\n"
        await message.answer(text)
    await state.clear()

# Удаление заметки
@note_router.message(F.text == "Удалить заметку")
async def delete_note_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    notes = note_service.get_notes(user_id)
    if not notes:
        await message.answer("❌ У вас нет заметок для удаления")
        return
    text = "🗑 Выберите номер заметки для удаления:\n\n"
    for i, note in enumerate(notes, start=1):
        text += f"{i}. {note.text} ({note.date} {note.time})\n"
    await state.set_state(NoteState.waiting_for_delete_index)
    await message.answer(text)

@note_router.message(NoteState.waiting_for_delete_index)
async def delete_note_process(message: Message, state: FSMContext):
    user_id = message.from_user.id
    try:
        index = int(message.text) - 1
    except ValueError:
        await message.answer("Введите номер заметки числом")
        return
    if note_service.delete_note(user_id, index):
        await message.answer("🗑 Заметка удалена")
    else:
        await message.answer("❌ Неверный номер заметки")
    await state.clear()
