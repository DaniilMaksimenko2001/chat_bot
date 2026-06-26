from openai import AsyncOpenAI
from core.config import PROXY_API

class AIService:
    def __init__(self, api_key: str = PROXY_API, base_url: str = "https://api.proxyapi.ru/openai/v1"):
        self.client = AsyncOpenAI(api_key=api_key,base_url=base_url)
        self.default_model = "gpt-4o-mini"
        self.system_instruction = "Отвечай кратко и по делу. Лимит - 2 предложения."

    async def ask_ai(self, text: str, model: str = None) -> str:
        target_model = model or self.default_model
        try:
            response = await self.client.chat.completions.create(
                model=target_model, 
                messages=[
                    {"role": "system", "content": self.system_instruction},
                    {"role": "user", "content": text}
                ],
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"ProxyAPI Error: {e}")
            return "⚠️ Произошла ошибка при обработке запроса нейросетью."