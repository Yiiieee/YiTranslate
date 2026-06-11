import requests

# 建立 Session 以重複使用連線，大幅加快 HTTPS 請求速度
session = requests.Session()

def translate_text(text, source_lang='auto', target_lang='zh-TW'):
    if not text.strip():
        return ""
    
    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        "client": "gtx",
        "sl": source_lang,
        "tl": target_lang,
        "dt": "t",
        "q": text
    }
    
    try:
        response = session.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        translated_text = ""
        if data and isinstance(data, list) and data[0]:
            for item in data[0]:
                if item[0]:
                    translated_text += item[0]
                    
        return translated_text
    except Exception as e:
        print(f"Translation API error: {e}")
        return "翻譯失敗，請檢查網路狀態。"