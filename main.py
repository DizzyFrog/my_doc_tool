# app.py
import multiprocessing
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from backend.excel_utils import excel_utils
from backend.mermaid_utils import is_mermaid_installed
from resource_util import resource_path
import os
import shutil
from dotenv import load_dotenv, set_key

load_dotenv(resource_path('.env'),override=True)
from mylog.log import logger

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("结构化文档批处理工具")
        self.iconphoto(True, tk.PhotoImage(file=resource_path("favo.png")))
        self.geometry("900x600")
        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="退出", command=self.quit)
        menubar.add_cascade(label="文件", menu=file_menu)
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="系统设置", command=self.open_settings)
        menubar.add_cascade(label="设置", menu=settings_menu)
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        self.config(menu=menubar)

    def create_widgets(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.Frame(main_frame, width=200)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 左侧按钮
        ttk.Button(left_frame, text="上传 Excel 文件", command=self.upload_excel).pack(fill=tk.X, pady=5)
        ttk.Button(left_frame, text="检查 Mermaid CLI", command=self.check_mermaid_cli).pack(fill=tk.X, pady=5)
        ttk.Button(left_frame, text="开始批量处理", command=self.start_batch).pack(fill=tk.X, pady=5)
        ttk.Button(left_frame, text="系统设置", command=self.open_settings).pack(fill=tk.X, pady=5)

        # 右侧内容
        ttk.Label(right_frame, text="处理进度/日志：").pack(anchor=tk.W)
        self.progress = ttk.Progressbar(right_frame, mode='determinate')
        self.progress.pack(fill=tk.X, pady=5)
        self.log_text = tk.Text(right_frame, height=20, state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=5)
        ttk.Button(right_frame, text="导出 docx 文件", command=self.export_docx).pack(anchor=tk.E, pady=5)

    def log(self, msg):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, msg + '\n')
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def check_mermaid_cli(self):
        if is_mermaid_installed():
            messagebox.showinfo("检查结果", "Mermaid CLI 已安装！")
        else:
            messagebox.showwarning("检查结果", "未检测到 Mermaid CLI，请先安装！")

    def upload_excel(self):
        file_path = filedialog.askopenfilename(title="选择Excel文件", filetypes=[("Excel Files", "*.xlsx *.xls")])
        if file_path:
            os.makedirs(resource_path('data/input'), exist_ok=True)
            new_path = resource_path(os.path.join('data', 'input', 'input.xlsx'))
            shutil.copy(file_path, new_path)
            sheets = excel_utils.get_excel_sheets()
            if not sheets:
                messagebox.showwarning("错误", "无法读取Excel文件或没有sheet页！")
                return
            sheet = simpledialog.askstring("选择 Sheet", f"可选Sheet: {', '.join(sheets)}\n请输入Sheet名称：")
            if sheet and sheet in sheets:
                # 保存到 .env
                set_key(resource_path('.env'), 'SHEET_NAME', sheet)
                messagebox.showinfo("成功", f"已选择Sheet: {sheet}，并保存到.env")
                self.log(f"已选择Sheet: {sheet}，并保存到.env")
            else:
                messagebox.showwarning("错误", "未选择有效Sheet！")

    def open_settings(self):
        # 可用 simpledialog 或自定义 Toplevel 实现设置弹窗
        pass

    def start_batch(self):
        self.log("开始批量处理...（此处补充你的处理逻辑）")

    def export_docx(self):
        self.log("导出 docx 文件...（此处补充你的导出逻辑）")

if __name__ == "__main__":
     # Pyinstaller fix
    multiprocessing.freeze_support()
    app = App()
    app.mainloop()