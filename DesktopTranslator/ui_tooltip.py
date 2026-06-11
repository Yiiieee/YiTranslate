import tkinter as tk

class TooltipWindow:
    def __init__(self):
        self.toplevel = None
        self.parent = None

    def init(self, parent):
        self.parent = parent

    def show(self, text, x, y):
        print(f"ui_tooltip: showing tooltip at {x}, {y} with text {text[:10]}")
        self.close()

        self.toplevel = tk.Toplevel(self.parent)
        self.toplevel.overrideredirect(True)
        self.toplevel.attributes('-topmost', True)
        self.toplevel.attributes('-alpha', 0.0) # 先隱藏視窗，避免排版計算時閃爍
        
        # 外層加上邊框顏色 (淺灰色)
        outer_frame = tk.Frame(self.toplevel, bg='#D0D0D0', cursor='fleur')
        outer_frame.pack(fill='both', expand=True)

        # 內層白色背景，營造 1px 邊框效果
        inner_frame = tk.Frame(outer_frame, bg='#FDFDFD', cursor='fleur')
        inner_frame.pack(fill='both', expand=True, padx=1, pady=1)

        # 移除前後多餘的空白或換行
        text = text.strip()

        # 使用 Label 元件取代 Text，Label 能完美貼合文字的像素大小，解決多餘空白的問題
        # wraplength=450 設定最大寬度，超過則自動換行
        text_widget = tk.Label(inner_frame, text=text, bg='#FDFDFD', fg='#202124', 
                               font=('Microsoft YaHei UI', 11), justify='left',
                               wraplength=450, padx=12, pady=12, cursor='fleur')
        text_widget.pack(expand=True, fill='both')

        # 將拖曳事件綁定到外層、內層與文字元件上，讓整個文本框都可以拖曳
        for widget in [outer_frame, inner_frame, text_widget]:
            widget.bind("<ButtonPress-1>", self.start_move)
            widget.bind("<B1-Motion>", self.do_move)

        # 再次更新以獲取真實像素大小
        self.toplevel.update()
        req_width = self.toplevel.winfo_reqwidth()
        req_height = self.toplevel.winfo_reqheight()
        
        screen_width = self.toplevel.winfo_screenwidth()
        screen_height = self.toplevel.winfo_screenheight()
        
        # 設定位置，滑鼠右下方一點點
        pos_x = x + 12
        pos_y = y + 12
        
        # 避免超出螢幕邊界，如果超過就往反方向彈出
        if pos_x + req_width > screen_width:
            pos_x = x - req_width - 5
        if pos_y + req_height > screen_height:
            pos_y = y - req_height - 5

        self.toplevel.geometry(f"+{int(pos_x)}+{int(pos_y)}")
        self.toplevel.attributes('-alpha', 1.0) # 排版定位完成，顯示視窗

        # 綁定事件：點擊視窗外或按下 ESC 關閉
        self.toplevel.bind('<FocusOut>', lambda e: self.close())
        self.toplevel.bind('<Escape>', lambda e: self.close())
        
        self.toplevel.focus_force()

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.toplevel.winfo_x() + deltax
        y = self.toplevel.winfo_y() + deltay
        self.toplevel.geometry(f"+{x}+{y}")

    def close(self):
        if self.toplevel:
            print("ui_tooltip: closing tooltip")
            try:
                self.toplevel.destroy()
            except:
                pass
            self.toplevel = None

_instance = TooltipWindow()

def init_tooltip(parent):
    _instance.init(parent)

def show_tooltip(text, x, y):
    _instance.show(text, x, y)