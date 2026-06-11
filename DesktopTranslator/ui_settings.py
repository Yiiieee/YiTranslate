import tkinter as tk
from tkinter import ttk, messagebox
import config_manager

LANGUAGES = {
    "自動偵測 (Auto-detect)": "auto",
    "繁體中文 (Traditional Chinese)": "zh-TW",
    "簡體中文 (Simplified Chinese)": "zh-CN",
    "英文 (English)": "en",
    "日文 (Japanese)": "ja",
    "韓文 (Korean)": "ko"
}

def get_lang_name(lang_code):
    for name, code in LANGUAGES.items():
        if code == lang_code:
            return name
    return "自動偵測 (Auto-detect)"

class SettingsWindow:
    def __init__(self, parent=None, on_save_callback=None):
        self.config = config_manager.load_config()
        self.on_save_callback = on_save_callback
        
        if parent:
            self.root = tk.Toplevel(parent)
        else:
            self.root = tk.Tk()
            
        self.root.title("Quick Translator 設定")
        self.root.geometry("350x250")
        self.root.resizable(False, False)
        
        # 設定視窗置中
        self.root.update_idletasks()
        width, height = 350, 250
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

        # --- Source Language ---
        tk.Label(self.root, text="來源語言:").grid(row=0, column=0, padx=20, pady=15, sticky='w')
        self.source_var = tk.StringVar(value=get_lang_name(self.config['source_lang']))
        self.source_cb = ttk.Combobox(self.root, textvariable=self.source_var, values=list(LANGUAGES.keys()), state='readonly', width=25)
        self.source_cb.grid(row=0, column=1, padx=10, pady=15)

        # --- Target Language ---
        tk.Label(self.root, text="目標語言:").grid(row=1, column=0, padx=20, pady=10, sticky='w')
        self.target_var = tk.StringVar(value=get_lang_name(self.config['target_lang']))
        target_langs = list(LANGUAGES.keys())
        target_langs.remove("自動偵測 (Auto-detect)") # 目標不能是自動偵測
        self.target_cb = ttk.Combobox(self.root, textvariable=self.target_var, values=target_langs, state='readonly', width=25)
        self.target_cb.grid(row=1, column=1, padx=10, pady=10)

        # --- Shortcut ---
        tk.Label(self.root, text="觸發快捷鍵:").grid(row=2, column=0, padx=20, pady=10, sticky='w')
        self.shortcut_entry = tk.Entry(self.root, width=28)
        self.shortcut_entry.insert(0, self.config['shortcut'])
        self.shortcut_entry.grid(row=2, column=1, padx=10, pady=10)
        
        # --- Save Button ---
        save_btn = tk.Button(self.root, text="儲存設定", command=self.save_settings, bg='#007bff', fg='white', font=('Arial', 10, 'bold'))
        save_btn.grid(row=3, column=0, columnspan=2, pady=20, ipadx=20)

    def save_settings(self):
        new_source = LANGUAGES.get(self.source_var.get(), 'auto')
        new_target = LANGUAGES.get(self.target_var.get(), 'zh-TW')
        new_shortcut = self.shortcut_entry.get().strip().lower()

        if not new_shortcut:
            messagebox.showerror("錯誤", "快捷鍵不能為空！")
            return

        self.config['source_lang'] = new_source
        self.config['target_lang'] = new_target
        self.config['shortcut'] = new_shortcut

        config_manager.save_config(self.config)
        messagebox.showinfo("成功", "設定已儲存！")
        
        if self.on_save_callback:
            self.on_save_callback()

    def run(self):
        self.root.attributes('-topmost', True) # Bring to front
        self.root.focus_force()
        # 只有在作為獨立視窗時才需要 mainloop
        if type(self.root) == tk.Tk:
            self.root.mainloop()

if __name__ == "__main__":
    SettingsWindow().run()