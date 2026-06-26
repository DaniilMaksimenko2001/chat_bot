from aiogram import Router,F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from services.cb_service import CBRService
from services.weather_service import WeatherService
from keyboards.main_keyboard import main_keyboard
from keyboards.info_keyboard import info_keyboard

cbr_service = CBRService()
weather_service = WeatherService()

class WeatherStates(StatesGroup):
    waiting_for_city = State()

info_router = Router()

@info_router.message(F.text == "Information")
async def message(message : Message):
    await message.answer("Information", reply_markup=info_keyboard)

@info_router.message(F.text == "Курсы валют")
async def message(message : Message):
    await message.answer(cbr_service.format_cbr_rates())

@info_router.message(F.text == "Погода")
async def message(message: Message, state: FSMContext):
    await message.answer("Введите название города:")
    await state.set_state(WeatherStates.waiting_for_city) # Перевод пользователя в состояние ожидания города

# Хэндлер который поймает текст сообщения, только если бот ждет город
@info_router.message(WeatherStates.waiting_for_city)
async def get_weather_handler(message: Message, state: FSMContext):
    city = message.text
    weather_report = weather_service.get_weather(city)
    await message.answer(weather_report)
    await state.clear()

@info_router.message(F.text == "Выход из модуля Information")
async def message(message: Message):
    await message.answer("Выход из модуля Information", reply_markup=main_keyboard)

