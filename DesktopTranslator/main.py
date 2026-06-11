import time
import threading
import keyboard
import pyperclip
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import ctypes
import queue
import tkinter as tk
import re

import config_manager
from translator import translate_text
import ui_tooltip
from ui_settings import SettingsWindow

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

def get_mouse_pos():
    pt = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y

def create_image():
    image = Image.new('RGB', (64, 64), color = '#007bff')
    dc = ImageDraw.Draw(image)
    dc.text((18, 12), "T", fill="white", font=None, align="center")
    return image

class AppLogic:
    def __init__(self):
        self.config = config_manager.load_config()
        self.tray_icon = None
        self.ui_queue = queue.Queue()
        
        # 建立隱藏的主視窗，負責跑 Tkinter mainloop
        self.root = tk.Tk()
        self.root.withdraw()
        
        # 初始化 tooltip，綁定到主視窗
        ui_tooltip.init_tooltip(self.root)
        
        self.setup_hotkey()
        
        # 啟動檢查 Queue 的迴圈 (用於在主執行緒中更新 UI)
        self.root.after(50, self.check_queue)
        
        # 啟動系統列 (背景執行)
        threading.Thread(target=self.run_tray, daemon=True).start()

    def check_queue(self):
        try:
            while True:
                task = self.ui_queue.get_nowait()
                print(f"check_queue: processing task {task['type']}")
                if task['type'] == 'show_tooltip':
                    ui_tooltip.show_tooltip(task['text'], task['x'], task['y'])
                elif task['type'] == 'show_settings':
                    SettingsWindow(self.root, on_save_callback=self.update_hotkey).run()
        except queue.Empty:
            pass
        self.root.after(50, self.check_queue)

    def setup_hotkey(self):
        try:
            keyboard.add_hotkey(self.config['shortcut'], self.on_activate)
            print(f"已綁定快捷鍵: {self.config['shortcut']}")
        except Exception as e:
            print(f"綁定快捷鍵失敗: {e}")

    def update_hotkey(self):
        keyboard.unhook_all_hotkeys()
        self.config = config_manager.load_config()
        self.setup_hotkey()

    def on_activate(self):
        # 使用一個 Thread 來處理抓取文字與網路請求
        threading.Thread(target=self.process_translation, daemon=True).start()

    def process_translation(self):
        old_clipboard = pyperclip.paste()
        pyperclip.copy("")
        
        # 稍微等待確保使用者已經放開快捷鍵，避免干擾 ctrl+c 的發送
        time.sleep(0.1)
        
        # 觸發複製
        keyboard.send('ctrl+c')
        
        # 增加等待時間並輪詢剪貼簿，因為 PDF 閱讀器複製文字通常較慢
        text = ""
        for _ in range(20):
            time.sleep(0.02)
            text = pyperclip.paste()
            if text.strip():
                break
        
        if not text.strip():
            pyperclip.copy(old_clipboard)
            return

        # --- 解決 PDF 複製時的斷行問題，大幅提升翻譯準確度 ---
        text = text.replace('\r', '')
        # 將單一換行取代為空白 (接續句子)，但保留雙換行 (段落)
        text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
        # -----------------------------------------------------

        print(f"準備翻譯: {text[:20]}...")
        
        # 呼叫翻譯 API
        translated = translate_text(text, self.config['source_lang'], self.config['target_lang'])
        
        # 取得游標位置
        x, y = get_mouse_pos()
        
        # 將顯示 UI 的任務丟回主執行緒
        self.ui_queue.put({'type': 'show_tooltip', 'text': translated, 'x': x, 'y': y})
        
        # 復原剪貼簿
        pyperclip.copy(old_clipboard)

    def open_settings(self, icon, item):
        self.ui_queue.put({'type': 'show_settings'})

    def exit_app(self, icon, item):
        keyboard.unhook_all_hotkeys()
        if self.tray_icon:
            self.tray_icon.stop()
        self.root.quit()

    def run_tray(self):
        menu = (
            item('設定', self.open_settings),
            item('離開', self.exit_app)
        )
        self.tray_icon = pystray.Icon("Quick Translator", create_image(), "Quick Translator", menu)
        print("Quick Translator 已啟動，縮小於系統列。")
        
        # 顯示啟動通知
        def on_setup(icon):
            icon.visible = True
            # 等待一下確保系統列圖示已建立
            time.sleep(0.5)
            try:
                icon.notify("桌面翻譯工具已在背景常駐。\n您可以框選文字並按下快捷鍵來翻譯！", title="啟動成功")
            except Exception as e:
                print(f"發送通知失敗: {e}")
                
        self.tray_icon.run(setup=on_setup)

    def run(self):
        # 啟動 Tkinter 主迴圈
        self.root.mainloop()

if __name__ == '__main__':
    app = AppLogic()
    app.run()