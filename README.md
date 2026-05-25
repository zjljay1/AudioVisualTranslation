# AudioVisualTranslation (实时音视频翻译工具)

![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)
![Chrome Extension](https://img.shields.io/badge/Chrome-Extension-green)
![PyQt6](https://img.shields.io/badge/PyQt6-Desktop-red)

一款跨平台的视频实时翻译工具。无论是浏览器中的网页视频（如 YouTube、B站），还是 Windows 桌面本地播放器（如 PotPlayer），本工具都能实时捕获音频，通过 AI 大模型进行语音识别与翻译，并为您展示美观的双语字幕。

## ✨ 核心特性

- **多场景覆盖**：支持浏览器网页音频捕获与 Windows 本地桌面音频捕获。
- **超低延迟**：通过异步音频切片与 WebSocket 流水线处理，实现 3 秒内的端到端识别与翻译。
- **高自由度字幕**：浏览器端和桌面端均支持字幕的随意拖拽、半透明防遮挡设计。
- **AI 强力驱动**：默认集成 OpenAI Whisper (语音识别) 和 GPT-4o-mini (翻译)，翻译结果符合口语习惯、更加地道。

## 📂 项目结构

项目分为三大核心模块：
- `backend/`: 核心本地服务端，负责音频处理、调用 ASR 与大语言模型翻译，以及 WebSocket 广播。
- `extension/`: Chrome/Edge 浏览器扩展，负责网页音频捕获与网页内字幕 DOM 渲染。
- `desktop_ui/`: 桌面客户端，基于 PyQt6 实现的透明置顶字幕悬浮窗。

*(更多关于技术架构的详细设计，请参阅 [ARCHITECTURE.md](./ARCHITECTURE.md))*

## 🚀 快速开始

### 1. 环境准备
- 确保已安装 **Python 3.12** 或以上版本。
- 准备一个有效的 OpenAI API Key（用于语音识别和翻译）。

### 2. 启动本地服务端 (Backend)

首先安装后端依赖并启动服务：

```bash
cd backend
pip install -r requirements.txt
```

接着，配置您的 API Key。详情请务必参考 👉 **[API 配置指南 (API_SETUP_GUIDE.md)](./API_SETUP_GUIDE.md)** 

配置完成后，启动服务：
```bash
python main.py
```
*(看到 `Starting AudioVisualTranslation WebSocket Server on ws://localhost:8765` 说明启动成功)*

### 3. 使用浏览器扩展 (Web 场景)

1. 打开 Chrome 或 Edge 浏览器，进入扩展管理页面 (`chrome://extensions/`)。
2. 开启右上角的 **"开发者模式"**。
3. 点击 **"加载已解压的扩展程序"**，选择本项目中的 `extension` 文件夹。
4. 打开任意视频网页（如 Bilibili），点击右上角扩展图标，在弹窗中点击 **"开始捕获并翻译"**。
5. 视频底部将出现可拖拽的双语字幕层！

### 4. 使用桌面悬浮字幕 (Desktop 场景)

如果您需要看本地视频或使用桌面客户端：

```bash
cd desktop_ui
pip install -r requirements.txt
python main_window.py
```
点击面板上的 **"开启桌面字幕"**，屏幕底部将出现一个鼠标可穿透、永远置顶的透明字幕窗口。

## 🛠️ 后续开发计划 (Roadmap)

- [ ] 集成 VAD (语音活动检测)，实现按语义断句切片。
- [ ] 接入本地 Faster-Whisper，实现 0 延迟、0 费用的本地离线语音识别。
- [ ] 接入本地 Ollama (Qwen2.5)，实现纯断网环境下的视频翻译。
- [ ] 优化 Windows WASAPI 桌面音频环回捕获模块。

## 📄 许可协议

MIT License