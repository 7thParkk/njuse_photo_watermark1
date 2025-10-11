"""
UI工具 - 提供GUI相关的辅助功能
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk, colorchooser, messagebox, filedialog
from typing import Callable, Optional, Any, List, Tuple
import os


class UIUtils:
    """UI工具类"""
    
    @staticmethod
    def center_window(window: tk.Tk | tk.Toplevel, width: int, height: int):
        """居中显示窗口"""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    @staticmethod
    def create_labeled_entry(
        parent: tk.Widget, 
        label_text: str, 
        entry_width: int = 20,
        row: int = None,
        column: int = 0,
        sticky: str = "ew"
    ) -> Tuple[ttk.Label, ttk.Entry]:
        """创建带标签的输入框"""
        label = ttk.Label(parent, text=label_text)
        entry = ttk.Entry(parent, width=entry_width)
        
        if row is not None:
            label.grid(row=row, column=column, sticky="w", padx=(0, 5))
            entry.grid(row=row, column=column + 1, sticky=sticky, padx=(0, 10))
        
        return label, entry
    
    @staticmethod
    def create_labeled_scale(
        parent: tk.Widget,
        label_text: str,
        from_: float,
        to: float,
        resolution: float = 1,
        orient: str = "horizontal",
        length: int = 200,
        command: Callable = None
    ) -> Tuple[ttk.Label, ttk.Scale]:
        """创建带标签的滑动条"""
        label = ttk.Label(parent, text=label_text)
        scale = ttk.Scale(
            parent,
            from_=from_,
            to=to,
            resolution=resolution,
            orient=orient,
            length=length,
            command=command
        )
        return label, scale
    
    @staticmethod
    def create_color_button(
        parent: tk.Widget,
        initial_color: str = "#FFFFFF",
        callback: Callable[[str], None] = None
    ) -> tk.Button:
        """创建颜色选择按钮"""
        color_var = tk.StringVar(value=initial_color)
        
        def choose_color():
            color = colorchooser.askcolor(initialcolor=color_var.get())
            if color[1]:  # 如果用户选择了颜色
                color_var.set(color[1])
                button.config(bg=color[1])
                if callback:
                    callback(color[1])
        
        button = tk.Button(
            parent,
            text="选择颜色",
            bg=initial_color,
            command=choose_color,
            relief="raised",
            bd=2
        )
        
        return button
    
    @staticmethod
    def create_position_grid(
        parent: tk.Widget,
        callback: Callable[[str], None] = None,
        initial_position: str = "bottom-right"
    ) -> tk.Frame:
        """创建九宫格位置选择器"""
        frame = ttk.Frame(parent)
        
        positions = [
            ["top-left", "top-center", "top-right"],
            ["center-left", "center", "center-right"],
            ["bottom-left", "bottom-center", "bottom-right"]
        ]
        
        position_var = tk.StringVar(value=initial_position)
        
        for i, row in enumerate(positions):
            for j, pos in enumerate(row):
                btn = ttk.Radiobutton(
                    frame,
                    text="●",
                    variable=position_var,
                    value=pos,
                    command=lambda p=pos: callback(p) if callback else None
                )
                btn.grid(row=i, column=j, padx=2, pady=2)
        
        return frame
    
    @staticmethod
    def show_error(title: str, message: str):
        """显示错误对话框"""
        messagebox.showerror(title, message)
    
    @staticmethod
    def show_warning(title: str, message: str):
        """显示警告对话框"""
        messagebox.showwarning(title, message)
    
    @staticmethod
    def show_info(title: str, message: str):
        """显示信息对话框"""
        messagebox.showinfo(title, message)
    
    @staticmethod
    def ask_yes_no(title: str, message: str) -> bool:
        """询问是否确认"""
        return messagebox.askyesno(title, message)
    
    @staticmethod
    def choose_files(
        title: str = "选择文件",
        filetypes: List[Tuple[str, str]] = None,
        multiple: bool = True
    ) -> List[str]:
        """选择文件"""
        if filetypes is None:
            filetypes = [
                ("图像文件", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif *.webp"),
                ("所有文件", "*.*")
            ]
        
        if multiple:
            files = filedialog.askopenfilenames(title=title, filetypes=filetypes)
            return list(files) if files else []
        else:
            file = filedialog.askopenfilename(title=title, filetypes=filetypes)
            return [file] if file else []
    
    @staticmethod
    def choose_directory(title: str = "选择文件夹", initialdir: str = None) -> str:
        """选择文件夹"""
        return filedialog.askdirectory(title=title, initialdir=initialdir) or ""
    
    @staticmethod
    def save_file(
        title: str = "保存文件",
        defaultextension: str = ".json",
        filetypes: List[Tuple[str, str]] = None
    ) -> str:
        """保存文件对话框"""
        if filetypes is None:
            filetypes = [("JSON文件", "*.json"), ("所有文件", "*.*")]
        
        return filedialog.asksaveasfilename(
            title=title,
            defaultextension=defaultextension,
            filetypes=filetypes
        ) or ""


class ProgressDialog:
    """进度对话框"""
    
    def __init__(self, parent: tk.Widget, title: str, message: str):
        self.parent = parent
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x150")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # 居中显示
        UIUtils.center_window(self.dialog, 400, 150)
        
        # 消息标签
        self.message_label = ttk.Label(self.dialog, text=message)
        self.message_label.pack(pady=10)
        
        # 进度条
        self.progress = ttk.Progressbar(
            self.dialog,
            mode='determinate',
            length=350
        )
        self.progress.pack(pady=10)
        
        # 详细信息标签
        self.detail_label = ttk.Label(self.dialog, text="")
        self.detail_label.pack(pady=5)
        
        # 取消按钮
        self.cancel_button = ttk.Button(
            self.dialog,
            text="取消",
            command=self.cancel
        )
        self.cancel_button.pack(pady=10)
        
        self.cancelled = False
    
    def update(self, current: int, total: int, detail: str = ""):
        """更新进度"""
        if self.cancelled:
            return False
        
        if total > 0:
            progress_value = (current / total) * 100
            self.progress['value'] = progress_value
        
        if detail:
            # 截断过长的文件路径
            if len(detail) > 50:
                detail = "..." + detail[-47:]
            self.detail_label.config(text=detail)
        
        self.dialog.update()
        return True
    
    def cancel(self):
        """取消操作"""
        self.cancelled = True
        self.close()
    
    def close(self):
        """关闭对话框"""
        self.dialog.destroy()
    
    def is_cancelled(self) -> bool:
        """检查是否被取消"""
        return self.cancelled


class ToolTip:
    """工具提示"""
    
    def __init__(self, widget: tk.Widget, text: str, delay: int = 500):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tooltip = None
        self.timer = None
        
        widget.bind("<Enter>", self.on_enter)
        widget.bind("<Leave>", self.on_leave)
        widget.bind("<ButtonPress>", self.on_leave)
    
    def on_enter(self, event=None):
        """鼠标进入"""
        self.timer = self.widget.after(self.delay, self.show_tooltip)
    
    def on_leave(self, event=None):
        """鼠标离开"""
        if self.timer:
            self.widget.after_cancel(self.timer)
            self.timer = None
        self.hide_tooltip()
    
    def show_tooltip(self):
        """显示提示"""
        if self.tooltip:
            return
        
        x, y, _, _ = self.widget.bbox("insert") if hasattr(self.widget, 'bbox') else (0, 0, 0, 0)
        x += self.widget.winfo_rootx() + 20
        y += self.widget.winfo_rooty() + 20
        
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = ttk.Label(
            self.tooltip,
            text=self.text,
            background="lightyellow",
            relief="solid",
            borderwidth=1,
            font=("Arial", 9)
        )
        label.pack()
    
    def hide_tooltip(self):
        """隐藏提示"""
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None