import asyncio
import logging
import io
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class ASREngine:
    def __init__(self, config):
        self.config = config
        self.engine_type = config.get("asr_engine", "whisper_api")
        
        # 尝试从 config.json 或环境变量中获取 API Key
        api_key = self.config.get("api_keys", {}).get("openai") or os.getenv("OPENAI_API_KEY")
        self.openai_client = AsyncOpenAI(api_key=api_key) if api_key else None

    async def transcribe_audio_chunk(self, audio_data: bytes) -> str:
        """
        接收音频数据块并进行识别
        """
        if self.engine_type == "whisper_api":
            return await self._transcribe_whisper_api(audio_data)
        elif self.engine_type == "faster_whisper":
            return await self._transcribe_faster_whisper(audio_data)
        else:
            logger.error(f"Unknown ASR engine: {self.engine_type}")
            return ""

    async def _transcribe_whisper_api(self, audio_data: bytes) -> str:
        if not self.openai_client:
            logger.error("OpenAI API Key not configured.")
            return "【请配置 OpenAI API Key】"
            
        try:
            # Whisper API 需要一个带有 filename 的文件对象
            audio_file = io.BytesIO(audio_data)
            audio_file.name = "audio.webm"  # 浏览器通常录制为 webm 格式
            
            response = await self.openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
            return response.strip()
        except Exception as e:
            logger.error(f"Whisper API error: {e}")
            return f"【识别错误: {str(e)}】"

    async def _transcribe_faster_whisper(self, audio_data: bytes) -> str:
        # TODO: 调用本地 faster-whisper 模型
        pass
