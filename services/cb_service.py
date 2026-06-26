import requests

class CBRService:
    def __init__(self):
        self.url = "https://www.cbr-xml-daily.ru/daily_json.js"

    def get_cbr_rates(self):
        try:
            data = requests.get(self.url, timeout=5).json()
            valutes = data.get("Valute", {})
            result = {
                "USD": valutes["USD"]["Value"],
                "EUR": valutes["EUR"]["Value"],
                "GBP": valutes["GBP"]["Value"],
                "CNY": valutes["CNY"]["Value"],
            }
            return result
        except Exception as e:
            print(f"CBR API Error: {e}")
            return None
        
    def format_cbr_rates(self):
        rates = self.get_cbr_rates()
        if not rates:
            return "⚠️ Не удалось получить данные ЦБ РФ."
        return (
            f"💱 Курсы валют ЦБ РФ:\n"
            f"🇺🇸 USD: {rates['USD']} руб.\n"
            f"🇪🇺 EUR: {rates['EUR']} руб.\n"
            f"🇬🇧 GBP: {rates['GBP']} руб.\n"
            f"🇨🇳 CNY: {rates['CNY']} руб."
        )