import requests
from core.config import OPEN_WEATHER_API

class WeatherService:
    def __init__(self):
        self.api_key = OPEN_WEATHER_API

    def get_weather(self, city: str) -> str:
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric&lang=ru"
            response = requests.get(url)
            data = response.json()
            
            # Ошибки API
            if response.status_code == 404:
                return "❌ Город не найден. Проверьте название."
            if response.status_code == 401:
                return "❌ Неверный API ключ."
            if response.status_code != 200:
                return f"⚠️ Ошибка сервера: {response.status_code}"
                
            # Данные
            name = data["name"]
            temp = data["main"]["temp"]
            feels = data["main"]["feels_like"]
            desc = data["weather"][0]["description"].capitalize()
            wind = data["wind"]["speed"]
            
            return (
                f"🌇 Погода в городе {name}:\n"
                f"{desc}\n"
                f"🌡 Температура: {temp}°C\n"
                f"❄️ Ощущается как: {feels}°C\n"
                f"💨 Ветер: {wind} м/с"
            )
        except requests.exceptions.ConnectionError:
            return "❌ Нет соединения с интернетом."
        except Exception as e:
            return f"⚠️ Ошибка: {e}"