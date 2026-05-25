import json
import os

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "source_language": "auto",
    "target_language": "zh",
    "asr_engine": "whisper_api", # 可选: whisper_api, faster_whisper, web_speech
    "translation_engine": "openai", # 可选: openai, deepl, google
    "api_keys": {
        "openai": "",
        "deepl": ""
    },
    "style": {
        "font_size": "24px",
        "color": "#FFFFFF",
        "background": "rgba(0, 0, 0, 0.5)"
    }
}

class ConfigManager:
    def __init__(self):
        self.config = DEFAULT_CONFIG.copy()
        self.load()

    def load(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                try:
                    user_config = json.load(f)
                    self.config.update(user_config)
                except Exception as e:
                    print(f"Error loading config: {e}")

    def save(self):
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)

    def update(self, new_config):
        self.config.update(new_config)
        self.save()

    def get(self, key, default=None):
        return self.config.get(key, default)

global_config = ConfigManager()
