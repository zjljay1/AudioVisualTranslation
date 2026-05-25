# AudioVisualTranslation - AI 辅助开发提示词与规范文档

本文档旨在为后续参与本项目的 AI 编程助手（或人类开发者）提供**全局上下文**、**代码规范**以及**功能扩展的提示词模板**。当您在一个全新的会话中希望 AI 继续开发本项目时，请先让 AI 阅读本文档。

---

## 1. AI 角色设定 (System Persona)

当要求 AI 开发此项目时，请使用或参考以下系统提示词：

> **【系统提示词】**
> 你是一位精通 Python 和 JavaScript 的高级全栈架构师。你现在负责开发和维护 `AudioVisualTranslation`（实时音视频翻译系统）。
> 该系统由三个部分组成：
> 1. `backend/`: 基于 Python `asyncio` 和 `websockets` 的本地核心中枢，负责处理音频流、调用 ASR (如 Whisper) 和 LLM (如 GPT-4o-mini)。
> 2. `extension/`: 基于 Manifest V3 的 Chrome 扩展，负责通过 `tabCapture` 捕获音频并分片，同时在 DOM 中渲染可拖拽的透明字幕。
> 3. `desktop_ui/`: 基于 PyQt6 的桌面透明置顶悬浮窗，通过 WebSocket 接收字幕并渲染。
> 
> **你的开发原则**：
> - 保持超低延迟（端到端 < 3秒），采用非阻塞的异步并发模型。
> - 代码必须包含详尽的 `logging` 日志和异常处理机制。
> - 在新增依赖时，必须同步更新对应的 `requirements.txt`。

---

## 2. 代码开发规范 (Coding Standards)

AI 在生成代码时，必须严格遵守以下规范：

### 2.1 Python 后端规范 (`backend/`)
- **异步优先**：涉及网络 I/O（如 API 调用、WebSocket 传输）、文件读写等操作，必须使用 `async/await`，绝不能阻塞事件循环。
- **模块解耦**：ASR 引擎和翻译引擎必须保持接口化。新增引擎时（如接入 Qwen、DeepL），只需在 `asr_engine.py` 或 `translator.py` 中新增 `_transcribe_xxx` 或 `_translate_xxx` 方法，不要破坏原有逻辑。
- **配置驱动**：所有的 API Key、模型名称、超时时间等，必须从 `config.py` 或 `.env` 读取，**严禁硬编码**。
- **错误降级**：当翻译或识别失败时，应捕获异常并返回带有明显标识的字符串（如 `【翻译失败: xxx】`），保证流水线不会崩溃。

### 2.2 浏览器扩展规范 (`extension/`)
- **Manifest V3 兼容**：后台脚本必须使用 `Service Worker` (`background.js`)，不可使用长期驻留的 DOM 或 `Window` 对象。
- **音频流处理**：使用 `MediaRecorder` 录制 WebM 格式。必须确保音频块是完整的、可独立解码的容器，避免后端 FFmpeg 解析失败。
- **DOM 隔离**：在 `content.js` 中注入的字幕 UI，其 CSS 必须具有足够高的优先级和极具辨识度的 ID（如 `#avt-subtitle-container`），防止与原网页样式冲突。

### 2.3 桌面端规范 (`desktop_ui/`)
- **线程安全**：WebSocket 网络通信必须放在独立的 `QThread` 中运行。UI 的更新必须通过 `pyqtSignal` 发射信号，**严禁在后台线程直接修改 UI 控件**。
- **无边框与穿透**：字幕窗口必须保持 `FramelessWindowHint` 和 `WindowStaysOnTopHint`，确保看视频时的沉浸感。

---

## 3. 功能扩展提示词模板 (Prompt Templates)

当您想让 AI 添加新功能时，可以直接复制以下提示词发送给 AI：

### 🎯 扩展目标 1：接入本地纯离线大模型 (Ollama)
> **提示词**：
> “请帮我修改 `backend/translator.py`，为其增加 Ollama 本地模型的支持。
> 需求：
> 1. 在 `config.py` 中增加 `translation_engine: "ollama"` 以及 `ollama_model: "qwen2.5:7b"` 的配置。
> 2. 使用 `aiohttp` 或 `openai` 兼容库调用本地的 `http://localhost:11434/v1/chat/completions` 接口。
> 3. 确保它是一个异步方法 `_translate_ollama`，并且处理好连接拒绝（ConnectionRefused）的异常捕获。”

### 🎯 扩展目标 2：接入本地 Faster-Whisper (离线语音识别)
> **提示词**：
> “请帮我完善 `backend/asr_engine.py` 中的 `_transcribe_faster_whisper` 方法。
> 需求：
> 1. 需要引入 `faster-whisper` 库（请更新 `requirements.txt`）。
> 2. 由于 Faster-Whisper 是 CPU/GPU 密集型且通常是同步阻塞的，请使用 `asyncio.to_thread()` 将其包装为异步调用，防止阻塞 WebSocket 事件循环。
> 3. 模型默认加载 `small` 尺寸，设备类型(device)根据是否安装 CUDA 自动判断为 `cuda` 或 `cpu`。
> 4. 音频输入是一个二进制的 WebM 字节流，请先使用 `io.BytesIO` 处理，再喂给模型。”

### 🎯 扩展目标 3：引入 VAD (语音活动检测) 优化音频切片
> **提示词**：
> “目前的浏览器扩展是固定每 2.5 秒切片一次，容易切断单词。请帮我使用 VAD 技术进行优化。
> 方案：在 `backend/main.py` 中引入 Silero VAD 或 WebRTC VAD。
> 需求：
> 1. 扩展端 `background.js` 改为发送连续的微小 PCM 音频流（例如每 100ms）。
> 2. 后端接收到音频流后，放入缓冲区。
> 3. 使用 VAD 检测缓冲区中的静音片段（Silence），只有当检测到明显的停顿，或者缓冲区达到 5 秒上限时，才截断音频送去 ASR 引擎识别。
> 4. 请给出详细的架构修改方案和代码实现。”

### 🎯 扩展目标 4：完善桌面端 WASAPI 音频捕获
> **提示词**：
> “请帮我编写 `backend/audio_capture.py`，实现 Windows 桌面的音频环回捕获。
> 需求：
> 1. 使用 `pyaudiowpatch` 库捕获系统发出的声音（WASAPI Loopback）。
> 2. 捕获到的音频流需要像浏览器扩展一样，切片（或者结合VAD）并推送到识别流水线中。
> 3. 确保该模块可以作为一个独立的后台任务与 `main.py` 的 WebSocket 服务同时运行。”

---

## 4. 常见排错指南 (Troubleshooting)

如果 AI 在后续开发中遇到 Bug，请让 AI 参考以下排错路径：
- **浏览器报错 `tabCapture` 为 null**：检查是否在 popup 中点击触发，因为 `tabCapture` 需要用户显式交互才能获取权限。
- **WebSocket 拒绝连接**：检查 Python 后端是否已成功启动并监听在 `8765` 端口；检查端口是否被其他应用占用。
- **Whisper 识别报错格式不支持**：浏览器发来的是 `webm` 封装的 Opus 编码音频，如果使用本地模型，可能需要使用 `pydub` 或 `ffmpeg-python` 将其在内存中转换为 `16kHz, 16-bit PCM` 格式。