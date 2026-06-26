import logging  
import asyncio  
from aiogram import Bot, Dispatcher, types  
from aiogram.filters import Command  
from aiogram.types import Message  
from core.config import TOKEN
from keyboards.main_keyboard import main_keyboard  
from notes import note_router
from ai import ai_router
from info import info_router

class TelegramBot:
    def __init__(self):
        self.api_token = TOKEN
        self.bot = Bot(token=self.api_token)  
        self.dp = Dispatcher()
        
        # Настройка логирования
        logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] >> %(message)s")
        
        # Регистрация хэндлеров и роутеров
        self._register_handlers()

    def _register_handlers(self):
        # Обработчик команды /start
        @self.dp.message(Command("start"))  
        async def send_welcome(message: Message):  
            await message.reply("Добрый день! Добро пожаловать!", reply_markup=main_keyboard)  

        # Хэндлер на команду /stop  
        @self.dp.message(Command('stop'))  
        async def cmd_stop(message: Message):  
            name = message.chat.first_name  
            await message.answer(f'Пока, {name}!')

        # Включение роутеров
        self.dp.include_router(info_router)
        self.dp.include_router(note_router)
        self.dp.include_router(ai_router)

    async def start(self):  
        await self.dp.start_polling(self.bot)  

if __name__ == '__main__':  
    telegram_bot = TelegramBot()
    asyncio.run(telegram_bot.start())