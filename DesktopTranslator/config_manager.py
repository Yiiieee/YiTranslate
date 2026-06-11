import json
import os

CONFIG_FILE = 'config.json'

DEFAULT_CONFIG = {
    'shortcut': 'ctrl+shift+y',
    'source_lang': 'auto',
    'target_lang': 'zh-TW'
}

def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
            # 確保缺少欄位時能補齊
            for k, v in DEFAULT_CONFIG.items():
                if k not in config:
                    config[k] = v
            return config
    except Exception as e:
        print(f"載入設定失敗: {e}")
        return DEFAULT_CONFIG

def save_config(config):
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"儲存設定失敗: {e}")