# AudioVisualTranslation 启动文档

本文档用于从零启动本项目的三个组成部分：

- `backend/`：本地 WebSocket 后端，负责语音识别和翻译。
- `extension/`：Chrome/Edge 浏览器扩展，负责捕获网页音频并显示网页字幕。
- `desktop_ui/`：桌面悬浮字幕窗口，负责接收后端字幕并显示在桌面上。

> 当前项目默认使用 OpenAI Whisper API 进行语音识别，使用 `gpt-4o-mini` 进行翻译。启动前需要准备可用的 `OPENAI_API_KEY`。

## 1. 环境要求

### 必需环境

- Windows 10/11
- Python 3.12 或更高版本
- Chrome 或 Edge 浏览器
- 可用的 OpenAI API Key

### 建议环境

- 使用 PowerShell 或 Windows Terminal 执行命令。
- 建议为后端和桌面端分别创建虚拟环境，避免污染全局 Python 环境。

如果 PowerShell 中中文显示为乱码，可以先执行：

```powershell
chcp 65001
```

## 2. 项目目录

假设项目位于：

```text
D:\code\project\AudioVisualTranslation
```

后续命令均以该目录为项目根目录。

```powershell
cd D:\code\project\AudioVisualTranslation
```

## 3. 配置 API Key

后端会从环境变量或 `config.json` 中读取 OpenAI API Key。推荐使用 `.env` 文件。

进入后端目录：

```powershell
cd D:\code\project\AudioVisualTranslation\backend
```

创建 `.env` 文件：

```env
OPENAI_API_KEY=sk-your-openai-api-key
```

如果使用 OpenAI 兼容代理，可以额外配置：

```env
OPENAI_API_KEY=sk-your-proxy-key
OPENAI_BASE_URL=https://your-proxy-domain/v1
```

更多 API 配置说明见 [API_SETUP_GUIDE.md](./API_SETUP_GUIDE.md)。

## 4. 启动后端服务

后端必须先启动，浏览器扩展和桌面端都会连接到：

```text
ws://localhost:8765
```

进入后端目录：

```powershell
cd D:\code\project\AudioVisualTranslation\backend
```

创建并启用虚拟环境：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

安装依赖：

```powershell
pip install -r requirements.txt
```

启动服务：

```powershell
python main.py
```

看到类似日志表示启动成功：

```text
Starting AudioVisualTranslation WebSocket Server on ws://localhost:8765
```

该窗口需要保持运行。关闭窗口或按 `Ctrl+C` 会停止后端服务。

## 5. 启动浏览器扩展

浏览器扩展用于网页视频场景，例如 Bilibili、YouTube、在线课程网页等。

### 安装扩展

1. 打开 Chrome 或 Edge。
2. 进入扩展管理页面：
   - Chrome：`chrome://extensions/`
   - Edge：`edge://extensions/`
3. 打开右上角的“开发者模式”。
4. 点击“加载已解压的扩展程序”。
5. 选择项目中的目录：

```text
D:\code\project\AudioVisualTranslation\extension
```

### 使用扩展

1. 确认后端服务已经启动。
2. 打开一个包含视频或音频的网页。
3. 点击浏览器右上角的扩展图标。
4. 选择源语言和目标语言。
5. 点击“开始捕获并翻译”。
6. 页面底部会出现可拖动的字幕区域。

停止时点击扩展弹窗中的“停止”。

### 注意事项

- 如果扩展无法连接后端，请确认 `python main.py` 正在运行。
- 如果浏览器提示无法捕获音频，请刷新目标网页后重新点击扩展按钮。
- 当前代码中的语言选择主要保存在浏览器本地存储中，后端配置更新逻辑仍在完善中；默认目标语言是中文 `zh`。

## 6. 启动桌面悬浮字幕

桌面端用于显示一个置顶字幕窗口。它不会主动捕获系统声音，当前主要作为字幕显示端，接收后端通过 WebSocket 广播的字幕。

保持后端服务运行，然后打开新的 PowerShell 窗口。

进入桌面端目录：

```powershell
cd D:\code\project\AudioVisualTranslation\desktop_ui
```

创建并启用虚拟环境：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

安装依赖：

```powershell
pip install -r requirements.txt
```

启动桌面控制窗口：

```powershell
python main_window.py
```

在控制窗口中点击“开启桌面字幕”，屏幕下方会显示悬浮字幕窗口。

## 7. 推荐启动顺序

日常使用建议按以下顺序启动：

1. 启动后端服务：

```powershell
cd D:\code\project\AudioVisualTranslation\backend
.\.venv\Scripts\Activate.ps1
python main.py
```

2. 加载或确认浏览器扩展已启用。

3. 打开视频网页，点击扩展开始捕获。

4. 如果需要桌面悬浮字幕，再启动桌面端：

```powershell
cd D:\code\project\AudioVisualTranslation\desktop_ui
.\.venv\Scripts\Activate.ps1
python main_window.py
```

## 8. 快速自检

### 检查后端端口

如果怀疑后端没有启动，可以执行：

```powershell
netstat -ano | findstr 8765
```

如果看到 `LISTENING`，说明 `8765` 端口正在被监听。

### 检查 Python 语法

在项目根目录执行：

```powershell
python -m py_compile backend\main.py backend\config.py backend\asr_engine.py backend\translator.py desktop_ui\main_window.py desktop_ui\overlay_window.py
```

没有输出通常表示语法检查通过。

### 检查扩展配置

在项目根目录执行：

```powershell
python -m json.tool extension\manifest.json
```

如果能正常输出格式化后的 JSON，说明扩展清单文件格式正确。

## 9. 常见问题

### 9.1 页面没有字幕

检查顺序：

1. 后端服务是否正在运行。
2. 浏览器扩展是否已经加载并启用。
3. 当前网页是否有正在播放的音频。
4. 是否已经点击“开始捕获并翻译”。
5. 后端窗口是否有识别或报错日志。

### 9.2 显示“请配置 OpenAI API Key”

说明后端没有读取到 API Key。检查：

1. `backend/.env` 是否存在。
2. `.env` 中是否有 `OPENAI_API_KEY=...`。
3. 修改 `.env` 后是否重启了后端服务。

### 9.3 WebSocket 连接失败

检查：

1. 后端是否启动。
2. `8765` 端口是否被其他程序占用。
3. 浏览器扩展是否访问的是 `ws://localhost:8765`。

### 9.4 PowerShell 里中文乱码

源码通常是正常的，可能只是控制台编码问题。执行：

```powershell
chcp 65001
```

或使用 Windows Terminal。

### 9.5 桌面字幕窗口没有内容

桌面端只负责显示后端广播的字幕。需要先有浏览器扩展或其他客户端向后端发送音频，后端完成识别和翻译后，桌面端才会显示字幕。

## 10. 关闭项目

关闭顺序建议：

1. 在浏览器扩展中点击“停止”。
2. 关闭桌面字幕窗口。
3. 在后端 PowerShell 窗口中按 `Ctrl+C` 停止服务。

