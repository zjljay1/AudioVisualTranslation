import asyncio
import json
import logging
import websockets
from config import global_config
from asr_engine import ASREngine
from translator import TranslationEngine

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 存储所有连接的客户端 (扩展、桌面UI等)
connected_clients = set()

# 初始化引擎
asr = ASREngine(global_config.config)
translator = TranslationEngine(global_config.config)

async def process_audio_pipeline(audio_data: bytes):
    """
    处理音频 -> 识别 -> 翻译 -> 广播
    """
    # 1. 语音识别
    original_text = await asr.transcribe_audio_chunk(audio_data)
    if not original_text or original_text.startswith("【"):
        # 忽略空文本或错误信息
        if original_text.startswith("【"):
            await broadcast_subtitle(original_text, original_text)
        return

    logger.info(f"Recognized: {original_text}")

    # 2. 翻译
    target_lang = global_config.get("target_language", "zh")
    translated_text = await translator.translate(original_text, target_lang)
    logger.info(f"Translated: {translated_text}")

    # 3. 广播给客户端
    await broadcast_subtitle(original_text, translated_text)

async def handler(websocket, path):
    """
    处理WebSocket连接、消息接收与分发
    """
    # 注册客户端
    connected_clients.add(websocket)
    logger.info(f"Client connected. Total clients: {len(connected_clients)}")
    
    try:
        async for message in websocket:
            # 判断消息类型 (文本或二进制音频流)
            if isinstance(message, str):
                try:
                    data = json.loads(message)
                    action = data.get("action")
                    
                    if action == "update_config":
                        logger.info(f"Received config update: {data}")
                        # TODO: 更新配置
                        
                    elif action == "start_transcription":
                        logger.info("Starting transcription...")
                        # TODO: 启动音频捕获与识别流程
                        
                    elif action == "stop_transcription":
                        logger.info("Stopping transcription...")
                        # TODO: 停止流程
                        
                except json.JSONDecodeError:
                    logger.warning("Received invalid JSON string.")
                    
            elif isinstance(message, bytes):
                # 收到完整的 WebM 音频块 (约2.5秒)
                # logger.debug(f"Received audio chunk of size {len(message)} bytes")
                # 启动后台任务处理流水线，不阻塞 WebSocket 接收
                asyncio.create_task(process_audio_pipeline(message))
                
    except websockets.exceptions.ConnectionClosed as e:
        logger.info(f"Client disconnected: {e}")
    finally:
        # 注销客户端
        connected_clients.remove(websocket)
        logger.info(f"Client removed. Total clients: {len(connected_clients)}")

async def broadcast_subtitle(original_text: str, translated_text: str):
    """
    将识别和翻译结果广播给所有连接的客户端 (如浏览器扩展和桌面字幕层)
    """
    if not connected_clients:
        return
        
    message = json.dumps({
        "type": "subtitle",
        "original": original_text,
        "translated": translated_text
    })
    
    # 并发发送给所有客户端
    await asyncio.gather(
        *[client.send(message) for client in connected_clients]
    )

async def main():
    logger.info("Starting AudioVisualTranslation WebSocket Server on ws://localhost:8765")
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # 永久运行

if __name__ == "__main__":
    asyncio.run(main())
