# AudioVisualTranslation API 配置指南

为了让实时视频翻译工具能够正常进行**语音识别 (ASR)** 和 **文本翻译**，您需要配置相应的 AI 服务 API Key。

本指南将指导您如何获取并配置 OpenAI API Key。

## 1. 为什么需要配置 API Key？

目前代码默认采用了 **方案 A：OpenAI Whisper API + gpt-4o-mini**。
- **Whisper API**：负责将视频中的声音提取出来，转换为文字（原文字幕）。
- **gpt-4o-mini**：负责将原文文字翻译成您选择的目标语言（如中文）。

如果不配置 API Key，工具虽然能捕获到音频并连接，但字幕上会显示 `【请配置 OpenAI API Key】`。

## 2. 如何获取 OpenAI API Key

如果您还没有 OpenAI API Key，可以通过以下步骤获取：

1. 访问 OpenAI 开发者平台: [https://platform.openai.com/](https://platform.openai.com/)
2. 注册或登录您的账号。
3. 确保您的账号绑定了支付方式（API 调用是按量计费的，Whisper $0.006/分钟，GPT-4o-mini 非常便宜）。
4. 导航到左侧菜单的 **API keys** 页面。
5. 点击 **"Create new secret key"**，为其命名（例如：`AudioTranslator`）。
6. 复制生成的 Key（一长串以 `sk-` 或 `sk-proj-` 开头的字符串）。**注意：关闭窗口后将无法再次查看此 Key，请务必保存好。**

> **替代方案提示**：
> 如果您因为网络原因无法使用官方 OpenAI API，也可以购买支持 OpenAI 格式的**国内 API 中转代理服务**（如 API2D、AI360 等），它们提供的 Key 和 Base URL 同样适用。

## 3. 如何配置 API Key 到本项目中

您可以通过以下两种方式之一步骤来配置：

### 方式一：使用 `.env` 文件 (推荐)

1. 在项目目录下的 `backend` 文件夹中，找到 `.env.example` 文件。
2. 将该文件重命名为 `.env`。
3. 使用文本编辑器打开 `.env` 文件。
4. 将 `your_openai_api_key_here` 替换为您刚刚复制的真实 API Key。

修改后的文件应该长这样：
```env
# OpenAI API Key (Required for Plan A)
OPENAI_API_KEY=sk-proj-1234567890abcdefghijklmnopqrstuvwxyz

# DeepL API Key (Optional)
DEEPL_API_KEY=
```

### 方式二：通过 `config.json` 配置

如果您之后使用了图形化界面（如我们准备的桌面控制中心），配置可能会保存在 `backend/config.json` 中：
```json
{
    "api_keys": {
        "openai": "sk-proj-1234567890abcdefghijklmnopqrstuvwxyz"
    }
}
```
*注：代码优先读取 `.env` 中的环境变量。*

## 4. 如何配置 API 代理地址 (可选，针对国内用户)

如果您使用了第三方中转 API（而非官方 `api.openai.com`），您需要在 `.env` 中添加一行 `OPENAI_BASE_URL`：

```env
OPENAI_API_KEY=sk-your-proxy-key
OPENAI_BASE_URL=https://api.your-proxy-provider.com/v1
```

*(注意：在我们的代码 `asr_engine.py` 和 `translator.py` 中，使用 `openai` 官方库时，它会自动读取环境变量中的 `OPENAI_BASE_URL` 并应用)*

## 5. 重启服务

完成上述修改后，您需要**重启后端的 Python 服务**（即重新运行 `backend/main.py`），新的 API Key 即可生效。