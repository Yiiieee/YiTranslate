<div align="center">
  <h1>🌐 YiTranslate (桌面翻譯小工具)</h1>
  <p><b>一個簡單、輕量 Windows 全域桌面翻譯工具</b></p>
</div>

<br/>

## 📖 專案簡介
**YiTranslate** 是一款常駐在 Windows 系統列的輕量化翻譯工具。  
無論你是在閱讀 PDF 論文、瀏覽網頁、還是撰寫程式，只要 **反白選取文字** 並按下 **快捷鍵**，翻譯結果就會瞬間在滑鼠游標的位置彈出，讓你能夠保持專注，不需頻繁切換視窗！


---

## ✨ 核心特色
- **🚀 全域快捷鍵翻譯**：在任何應用程式中選取文字，按下 `Ctrl + Shift + Y`（預設），立刻顯示翻譯結果。
- **🎯 游標跟隨**：翻譯結果會以簡潔的 Tooltip 視窗直接顯示在你的滑鼠游標旁邊，閱讀體驗極佳。
- **📄 智慧 PDF 換行修復**：自動修復 PDF 文字複製時產生的破碎斷行，保留真實段落，翻譯不再支離破碎。
- **⚙️ 輕量可自訂**：常駐於系統工作列 (System Tray)，不佔用工作列空間。提供簡潔設定介面，可自訂「快捷鍵」、「來源語言」及「目標語言」。
- **⚡ 快速且免費**：串接 Google Translate API，翻譯速度快且無須額外設定 API Key。

---

## 🛠️ 開發技術棧
- **Python 3**
- `keyboard`：監聽全域快捷鍵
- `pyperclip`：剪貼簿操作與讀取
- `requests`：處理翻譯 API 請求
- `pystray` / `Pillow`：系統列圖示管理
- `tkinter`：輕量級 GUI (用於 Tooltip 及設定視窗)

---

## 🚀 如何使用與安裝

### 方法一：使用打包好的執行檔 

1. 雙擊執行 `QuickTranslator.exe`。
2. 在右下角系統列 (System Tray) 會看到一個藍色的圖示。
3. 反白任何想翻譯的文字，按下預設快捷鍵 `Ctrl + Shift + Y`，即可看到翻譯結果。

### 方法二：從源碼執行 

1. **複製專案：**
   ```bash
   git clone https://github.com/Yiiieee/YiTranslate.git
   cd DesktopTranslator
   ```
2. **安裝依賴套件：**
   ```bash
   pip install -r requirements.txt
   ```
3. **執行程式：**
   ```bash
   python main.py
   ```

---

## ⚙️ 設定與自訂
在系統列對著藍色 `T` 圖示按 **右鍵**，選擇 **「設定」**，即可開啟設定視窗：
- **快捷鍵**：點擊輸入框後，按下你想要設定的新快捷鍵（例如 `alt+t`）。
- **來源語言**：預設為 `auto` (自動偵測)。
- **目標語言**：預設為 `zh-TW` (繁體中文)。

*所有設定會自動儲存在專案目錄下的 `config.json` 檔案中。*

---

## 📦 如何打包成 .exe 執行檔
如果你想要自己將原始碼打包為 Windows 獨立執行檔，專案內已提供了 `QuickTranslator.spec` 檔案，請依照以下步驟：

1. 安裝 PyInstaller：
   ```bash
   pip install pyinstaller
   ```
2. 執行打包指令：
   ```bash
   pyinstaller QuickTranslator.spec
   ```
3. 打包完成後，可以在 `dist/` 資料夾中找到 `QuickTranslator.exe`。

---

## 🤝 貢獻與反饋
歡迎提出 Issue 或是提交 Pull Request 來讓這個小工具變得更好！如果你覺得這個工具有幫助到你，請不要吝嗇給予一顆 ⭐ **Star**！
