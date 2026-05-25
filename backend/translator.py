import asyncio
import logging
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class TranslationEngine:
    def __init__(self, config):
        self.config = config
        self.engine_type = config.get("translation_engine", "openai")
        
        api_key = self.config.get("api_keys", {}).get("openai") or os.getenv("OPENAI_API_KEY")
        self.openai_client = AsyncOpenAI(api_key=api_key) if api_key else None

    async def translate(self, text: str, target_lang: str) -> str:
        """
        将文本翻译为目标语言
        """
        if not text:
            return ""
            
        if self.engine_type == "openai":
            return await self._translate_openai(text, target_lang)
        elif self.engine_type == "deepl":
            return await self._translate_deepl(text, target_lang)
        else:
            logger.error(f"Unknown Translation engine: {self.engine_type}")
            return text

    async def _translate_openai(self, text: str, target_lang: str) -> str:
        if not self.openai_client:
            return "【请配置 OpenAI API Key】"
            
        try:
            system_prompt = f"你是一个专业的字幕翻译专家。请将以下文本翻译为{target_lang}。要求：符合口语习惯，短小精悍，不要解释，直接输出翻译结果。"
            
            response = await self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text}
                ],
                temperature=0.3,
                max_tokens=100
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"OpenAI Translation error: {e}")
            return f"【翻译错误: {str(e)}】"

    async def _translate_deepl(self, text: str, target_lang: str) -> str:
        # TODO: 调用 DeepL API
        pass
