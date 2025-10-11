"""
主窗口 - GUI应用的主界面
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
from typing import List, Optional
from PIL import Image

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from core.watermark_engine import WatermarkEngine
from core.template import TemplateManager, SettingsManager
from core.image_processor import ImageProcessor
from utils.ui_utils import UIUtils, ToolTip
from utils.file_utils import FileUtils, ImageCache


class MainWindow:
    """主窗口类"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("照片水印工具 v1.0")
        self.root.geometry("1200x800")
        
        # 设置窗口图标（如果有的话）
        try:
            icon_path = os.path.join(project_root, "resources", "icon.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass
        
        # 核心组件
        self.watermark_engine = WatermarkEngine()
        self.template_manager = TemplateManager()
        self.settings_manager = SettingsManager()
        self.image_processor = ImageProcessor()
        self.image_cache = ImageCache()
        
        # 界面变量
        self.current_images: List[str] = []
        self.current_image_index = 0
        self.preview_image = None
        
        # 界面组件引用
        self.file_listbox = None
        self.preview_canvas = None
        self.template_combobox = None
        
        # 创建界面
        self.create_menu()
        self.create_main_layout()
        self.setup_bindings()
        
        # 加载设置
        self.load_settings()
        
        # 设置退出处理
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件(F)", menu=file_menu)
        file_menu.add_command(label="导入图片...", command=self.import_images, accelerator="Ctrl+O")
        file_menu.add_command(label="导入文件夹...", command=self.import_folder, accelerator="Ctrl+Shift+O")
        file_menu.add_separator()
        file_menu.add_command(label="导出水印图片...", command=self.export_images, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.on_closing, accelerator="Ctrl+Q")
        
        # 编辑菜单
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="编辑(E)", menu=edit_menu)
        edit_menu.add_command(label="清空图片列表", command=self.clear_images)
        edit_menu.add_separator()
        edit_menu.add_command(label="复制当前设置", command=self.copy_settings)
        edit_menu.add_command(label="粘贴设置", command=self.paste_settings)
        
        # 模板菜单
        template_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="模板(T)", menu=template_menu)
        template_menu.add_command(label="新建模板...", command=self.new_template)
        template_menu.add_command(label="保存当前设置为模板...", command=self.save_as_template)
        template_menu.add_separator()
        template_menu.add_command(label="管理模板...", command=self.manage_templates)
        template_menu.add_separator()
        template_menu.add_command(label="导入模板...", command=self.import_template)
        template_menu.add_command(label="导出模板...", command=self.export_template)
        
        # 视图菜单
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="视图(V)", menu=view_menu)
        view_menu.add_command(label="刷新预览", command=self.refresh_preview, accelerator="F5")
        view_menu.add_command(label="适应窗口", command=self.fit_preview_to_window)
        view_menu.add_command(label="实际大小", command=self.actual_size_preview)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助(H)", menu=help_menu)
        help_menu.add_command(label="使用说明", command=self.show_help)
        help_menu.add_command(label="关于", command=self.show_about)
    
    def create_main_layout(self):
        """创建主界面布局"""
        # 创建主容器
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 左侧面板
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=1)
        
        # 右侧面板
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=2)
        
        # 创建左侧内容
        self.create_left_panel(left_frame)
        
        # 创建右侧内容
        self.create_right_panel(right_frame)
    
    def create_left_panel(self, parent):
        """创建左侧面板（文件列表和设置）"""
        # 文件列表区域
        file_frame = ttk.LabelFrame(parent, text="图片文件", padding=5)
        file_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        # 工具栏
        toolbar = ttk.Frame(file_frame)
        toolbar.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(toolbar, text="导入图片", command=self.import_images).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="导入文件夹", command=self.import_folder).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="清空", command=self.clear_images).pack(side=tk.LEFT)
        
        # 文件列表
        list_frame = ttk.Frame(file_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 列表框
        self.file_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            selectmode=tk.SINGLE
        )
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.file_listbox.yview)
        
        # 绑定选择事件
        self.file_listbox.bind('<<ListboxSelect>>', self.on_file_select)
        
        # 设置区域
        settings_frame = ttk.LabelFrame(parent, text="水印设置", padding=5)
        settings_frame.pack(fill=tk.X)
        
        self.create_settings_panel(settings_frame)
    
    def create_settings_panel(self, parent):
        """创建设置面板"""
        # 模板选择
        template_frame = ttk.Frame(parent)
        template_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(template_frame, text="模板:").pack(side=tk.LEFT)
        self.template_combobox = ttk.Combobox(
            template_frame,
            state="readonly",
            width=15
        )
        self.template_combobox.pack(side=tk.LEFT, padx=(5, 0), fill=tk.X, expand=True)
        self.template_combobox.bind('<<ComboboxSelected>>', self.on_template_select)
        
        # 更新模板列表
        self.update_template_list()
        
        # 水印文本
        text_frame = ttk.Frame(parent)
        text_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(text_frame, text="水印文本:").pack(anchor=tk.W)
        self.text_entry = ttk.Entry(text_frame)
        self.text_entry.pack(fill=tk.X, pady=(2, 0))
        self.text_entry.bind('<KeyRelease>', self.on_settings_change)
        
        # 字体大小
        size_frame = ttk.Frame(parent)
        size_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(size_frame, text="字体大小:").pack(side=tk.LEFT)
        self.size_var = tk.IntVar(value=32)
        size_scale = ttk.Scale(
            size_frame,
            from_=10,
            to=100,
            variable=self.size_var,
            orient=tk.HORIZONTAL,
            command=self.on_settings_change
        )
        size_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        
        self.size_label = ttk.Label(size_frame, text="32")
        self.size_label.pack(side=tk.RIGHT)
        
        # 颜色选择
        color_frame = ttk.Frame(parent)
        color_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(color_frame, text="颜色:").pack(side=tk.LEFT)
        self.color_button = UIUtils.create_color_button(
            color_frame,
            initial_color="#FFFFFF",
            callback=self.on_color_change
        )
        self.color_button.pack(side=tk.LEFT, padx=(5, 0))
        
        # 透明度
        alpha_frame = ttk.Frame(parent)
        alpha_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(alpha_frame, text="透明度:").pack(side=tk.LEFT)
        self.alpha_var = tk.IntVar(value=100)
        alpha_scale = ttk.Scale(
            alpha_frame,
            from_=10,
            to=100,
            variable=self.alpha_var,
            orient=tk.HORIZONTAL,
            command=self.on_settings_change
        )
        alpha_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        
        self.alpha_label = ttk.Label(alpha_frame, text="100%")
        self.alpha_label.pack(side=tk.RIGHT)
        
        # 位置选择
        pos_frame = ttk.LabelFrame(parent, text="位置", padding=5)
        pos_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.position_frame = UIUtils.create_position_grid(
            pos_frame,
            callback=self.on_position_change,
            initial_position="bottom-right"
        )
        self.position_frame.pack()
        
        # 边距
        margin_frame = ttk.Frame(parent)
        margin_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(margin_frame, text="边距:").pack(side=tk.LEFT)
        self.margin_var = tk.IntVar(value=16)
        margin_scale = ttk.Scale(
            margin_frame,
            from_=0,
            to=100,
            variable=self.margin_var,
            orient=tk.HORIZONTAL,
            command=self.on_settings_change
        )
        margin_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        
        self.margin_label = ttk.Label(margin_frame, text="16px")
        self.margin_label.pack(side=tk.RIGHT)
        
        # 高级设置区域（可折叠）
        advanced_frame = ttk.LabelFrame(parent, text="高级设置", padding=5)
        advanced_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 旋转角度
        rotation_frame = ttk.Frame(advanced_frame)
        rotation_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(rotation_frame, text="旋转:").pack(side=tk.LEFT)
        self.rotation_var = tk.IntVar(value=0)
        rotation_scale = ttk.Scale(
            rotation_frame,
            from_=-180,
            to=180,
            variable=self.rotation_var,
            orient=tk.HORIZONTAL,
            command=self.on_settings_change
        )
        rotation_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        
        self.rotation_label = ttk.Label(rotation_frame, text="0°")
        self.rotation_label.pack(side=tk.RIGHT)
        
        # 阴影设置
        shadow_frame = ttk.Frame(advanced_frame)
        shadow_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.shadow_var = tk.BooleanVar(value=True)
        shadow_check = ttk.Checkbutton(
            shadow_frame,
            text="启用阴影",
            variable=self.shadow_var,
            command=self.on_settings_change
        )
        shadow_check.pack(side=tk.LEFT)
        
        # 描边设置
        stroke_frame = ttk.Frame(advanced_frame)
        stroke_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.stroke_var = tk.BooleanVar(value=False)
        stroke_check = ttk.Checkbutton(
            stroke_frame,
            text="启用描边",
            variable=self.stroke_var,
            command=self.on_settings_change
        )
        stroke_check.pack(side=tk.LEFT)
        
        # 操作按钮
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(
            button_frame,
            text="应用到当前",
            command=self.apply_to_current
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            button_frame,
            text="批量导出",
            command=self.export_images
        ).pack(side=tk.RIGHT)
    
    def create_right_panel(self, parent):
        """创建右侧面板（预览区域）"""
        preview_frame = ttk.LabelFrame(parent, text="预览", padding=5)
        preview_frame.pack(fill=tk.BOTH, expand=True)
        
        # 预览工具栏
        preview_toolbar = ttk.Frame(preview_frame)
        preview_toolbar.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(preview_toolbar, text="上一张", command=self.prev_image).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(preview_toolbar, text="下一张", command=self.next_image).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(preview_toolbar, text="刷新", command=self.refresh_preview).pack(side=tk.LEFT)
        
        # 图片信息标签
        self.info_label = ttk.Label(preview_toolbar, text="无图片")
        self.info_label.pack(side=tk.RIGHT)
        
        # 预览画布
        self.preview_canvas = tk.Canvas(
            preview_frame,
            bg="gray90",
            relief=tk.SUNKEN,
            bd=2
        )
        self.preview_canvas.pack(fill=tk.BOTH, expand=True)
        
        # 添加滚动条
        h_scroll = ttk.Scrollbar(preview_frame, orient=tk.HORIZONTAL, command=self.preview_canvas.xview)
        v_scroll = ttk.Scrollbar(preview_frame, orient=tk.VERTICAL, command=self.preview_canvas.yview)
        
        self.preview_canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)
    
    def setup_bindings(self):
        """设置快捷键绑定"""
        self.root.bind('<Control-o>', lambda e: self.import_images())
        self.root.bind('<Control-O>', lambda e: self.import_folder())
        self.root.bind('<Control-s>', lambda e: self.export_images())
        self.root.bind('<Control-q>', lambda e: self.on_closing())
        self.root.bind('<F5>', lambda e: self.refresh_preview())
        
        # 方向键切换图片
        self.root.bind('<Left>', lambda e: self.prev_image())
        self.root.bind('<Right>', lambda e: self.next_image())
        self.root.bind('<Up>', lambda e: self.prev_image())
        self.root.bind('<Down>', lambda e: self.next_image())
    
    def run(self):
        """运行应用"""
        self.root.mainloop()
    
    # 文件管理方法
    def import_images(self):
        """导入图片文件"""
        files = UIUtils.choose_files(
            title="选择图片文件",
            filetypes=[
                ("图像文件", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif *.webp"),
                ("所有文件", "*.*")
            ],
            multiple=True
        )
        
        if files:
            self.add_images(files)
    
    def import_folder(self):
        """导入文件夹中的图片"""
        folder = UIUtils.choose_directory(title="选择包含图片的文件夹")
        if folder:
            try:
                # 收集文件夹中的图片
                files = self.image_processor.collect_image_files(folder, recursive=False)
                if files:
                    self.add_images(files)
                else:
                    UIUtils.show_info("提示", "所选文件夹中没有找到支持的图片文件")
            except Exception as e:
                UIUtils.show_error("错误", f"导入文件夹失败：{str(e)}")
    
    def add_images(self, file_paths: list):
        """添加图片到列表"""
        added_count = 0
        for file_path in file_paths:
            if file_path not in self.current_images:
                # 验证图片文件
                is_valid, message = FileUtils.validate_image_file(file_path)
                if is_valid:
                    self.current_images.append(file_path)
                    # 添加到列表框显示
                    filename = os.path.basename(file_path)
                    self.file_listbox.insert(tk.END, filename)
                    added_count += 1
                else:
                    print(f"跳过无效图片: {file_path} - {message}")
        
        if added_count > 0:
            # 选择第一张图片
            if len(self.current_images) == added_count:  # 第一次添加
                self.current_image_index = 0
                self.file_listbox.selection_set(0)
                self.update_preview()
            
            self.update_info_label()
        
        if added_count == 0 and file_paths:
            UIUtils.show_warning("警告", "没有找到有效的图片文件")
    
    def clear_images(self):
        """清空图片列表"""
        if self.current_images and UIUtils.ask_yes_no("确认", "确定要清空所有图片吗？"):
            self.current_images.clear()
            self.file_listbox.delete(0, tk.END)
            self.current_image_index = 0
            self.preview_canvas.delete("all")
            self.info_label.config(text="无图片")
            self.image_cache.clear()
    
    def on_file_select(self, event):
        """文件列表选择事件"""
        selection = self.file_listbox.curselection()
        if selection:
            self.current_image_index = selection[0]
            self.update_preview()
    
    def prev_image(self):
        """上一张图片"""
        if self.current_images and self.current_image_index > 0:
            self.current_image_index -= 1
            self.file_listbox.selection_clear(0, tk.END)
            self.file_listbox.selection_set(self.current_image_index)
            self.file_listbox.see(self.current_image_index)
            self.update_preview()
    
    def next_image(self):
        """下一张图片"""
        if self.current_images and self.current_image_index < len(self.current_images) - 1:
            self.current_image_index += 1
            self.file_listbox.selection_clear(0, tk.END)
            self.file_listbox.selection_set(self.current_image_index)
            self.file_listbox.see(self.current_image_index)
            self.update_preview()
    
    def update_info_label(self):
        """更新图片信息标签"""
        if self.current_images:
            current = self.current_image_index + 1
            total = len(self.current_images)
            current_file = self.current_images[self.current_image_index]
            filename = os.path.basename(current_file)
            self.info_label.config(text=f"{current}/{total} - {filename}")
        else:
            self.info_label.config(text="无图片")
    
    # 预览相关方法
    def update_preview(self):
        """更新预览"""
        if not self.current_images:
            self.preview_canvas.delete("all")
            return
        
        current_file = self.current_images[self.current_image_index]
        self.update_info_label()
        
        try:
            # 检查缓存
            cache_key = f"{current_file}:preview"
            preview_image = self.image_cache.get(cache_key)
            
            if preview_image is None:
                # 加载并应用水印
                with self.image_processor.load_image(current_file) as img:
                    # 获取日期文本
                    date_text = self.image_processor.get_date_text_for_image(
                        current_file, 
                        self.watermark_engine.settings.get('text', 'YYYY-MM-DD')
                    )
                    
                    # 应用水印（预览模式）
                    preview_image = self.watermark_engine.apply_watermark(
                        img, 
                        text=date_text or self.text_entry.get(),
                        preview_mode=True
                    )
                    
                    # 缓存预览图像
                    self.image_cache.put(cache_key, preview_image)
            
            # 显示在画布上
            self.display_image_on_canvas(preview_image)
            
        except Exception as e:
            print(f"预览更新失败: {e}")
            self.preview_canvas.delete("all")
            # 在画布上显示错误信息
            self.preview_canvas.create_text(
                self.preview_canvas.winfo_width() // 2,
                self.preview_canvas.winfo_height() // 2,
                text=f"预览失败: {str(e)}",
                fill="red",
                font=("Arial", 12)
            )
    
    def display_image_on_canvas(self, pil_image):
        """在画布上显示PIL图像"""
        try:
            from PIL import ImageTk
            
            # 转换为Tkinter可显示的格式
            tk_image = ImageTk.PhotoImage(pil_image)
            
            # 清空画布
            self.preview_canvas.delete("all")
            
            # 计算显示位置（居中）
            canvas_width = self.preview_canvas.winfo_width()
            canvas_height = self.preview_canvas.winfo_height()
            
            image_width = tk_image.width()
            image_height = tk_image.height()
            
            x = max(0, (canvas_width - image_width) // 2)
            y = max(0, (canvas_height - image_height) // 2)
            
            # 在画布上显示图像
            self.preview_canvas.create_image(x, y, anchor=tk.NW, image=tk_image)
            
            # 保存引用防止垃圾回收
            self.preview_canvas.image = tk_image
            
            # 设置滚动区域
            self.preview_canvas.configure(scrollregion=self.preview_canvas.bbox("all"))
            
        except Exception as e:
            print(f"显示图像失败: {e}")
    
    def refresh_preview(self):
        """刷新预览"""
        if self.current_images:
            # 清除缓存以强制重新生成
            current_file = self.current_images[self.current_image_index]
            cache_key = f"{current_file}:preview"
            self.image_cache.remove(cache_key)
            self.update_preview()
    
    def fit_preview_to_window(self):
        """适应窗口大小"""
        # TODO: 实现缩放适应窗口功能
        pass
    
    def actual_size_preview(self):
        """实际大小预览"""
        # TODO: 实现实际大小预览功能
        pass
    
    # 设置相关方法
    def on_template_select(self, event):
        """模板选择事件"""
        template_name = self.template_combobox.get()
        if template_name:
            template = self.template_manager.get_template(template_name)
            if template:
                # 应用模板设置
                self.apply_template_settings(template.settings)
                self.refresh_preview()
    
    def apply_template_settings(self, settings: dict):
        """应用模板设置到UI"""
        # 更新水印引擎设置
        self.watermark_engine.update_settings(**settings)
        
        # 更新UI控件
        self.text_entry.delete(0, tk.END)
        self.text_entry.insert(0, settings.get('text', ''))
        
        self.size_var.set(settings.get('font_size', 32))
        self.size_label.config(text=str(settings.get('font_size', 32)))
        
        self.alpha_var.set(settings.get('transparency', 100))
        self.alpha_label.config(text=f"{settings.get('transparency', 100)}%")
        
        self.margin_var.set(settings.get('margin_x', 16))
        self.margin_label.config(text=f"{settings.get('margin_x', 16)}px")
        
        # 高级设置
        self.rotation_var.set(settings.get('rotation', 0))
        self.rotation_label.config(text=f"{settings.get('rotation', 0)}°")
        
        self.shadow_var.set(settings.get('shadow_enabled', True))
        self.stroke_var.set(settings.get('stroke_enabled', False))
        
        # 更新颜色按钮
        color = settings.get('color', '#FFFFFF')
        self.color_button.config(bg=color)
    
    def on_settings_change(self, event=None):
        """设置改变事件"""
        try:
            # 更新水印引擎设置
            self.watermark_engine.update_settings(
                text=self.text_entry.get(),
                font_size=int(self.size_var.get()),
                transparency=int(self.alpha_var.get()),
                margin_x=int(self.margin_var.get()),
                margin_y=int(self.margin_var.get()),
                rotation=int(self.rotation_var.get()),
                shadow_enabled=self.shadow_var.get(),
                stroke_enabled=self.stroke_var.get()
            )
            
            # 更新标签
            self.size_label.config(text=str(int(self.size_var.get())))
            self.alpha_label.config(text=f"{int(self.alpha_var.get())}%")
            self.margin_label.config(text=f"{int(self.margin_var.get())}px")
            self.rotation_label.config(text=f"{int(self.rotation_var.get())}°")
            
            # 刷新预览
            self.refresh_preview()
            
        except Exception as e:
            print(f"设置更新失败: {e}")
    
    def on_color_change(self, color):
        """颜色改变事件"""
        self.watermark_engine.update_settings(color=color)
        self.refresh_preview()
    
    def on_position_change(self, position):
        """位置改变事件"""
        self.watermark_engine.update_settings(position=position)
        self.refresh_preview()
    
    def apply_to_current(self):
        """应用水印到当前图片"""
        if not self.current_images:
            UIUtils.show_warning("警告", "请先导入图片文件")
            return
        
        current_file = self.current_images[self.current_image_index]
        
        # 选择输出文件
        output_file = UIUtils.save_file(
            title="保存水印图片",
            defaultextension=".jpg",
            filetypes=[
                ("JPEG图像", "*.jpg"),
                ("PNG图像", "*.png"),
                ("所有文件", "*.*")
            ]
        )
        
        if output_file:
            try:
                # 加载原图像
                with self.image_processor.load_image(current_file) as img:
                    # 获取日期文本
                    date_text = self.image_processor.get_date_text_for_image(
                        current_file,
                        self.watermark_engine.settings.get('text', 'YYYY-MM-DD')
                    )
                    
                    # 应用水印（非预览模式）
                    watermarked = self.watermark_engine.apply_watermark(
                        img,
                        text=date_text or self.text_entry.get(),
                        preview_mode=False
                    )
                    
                    # 保存图像
                    save_format = os.path.splitext(output_file)[1].lstrip('.').upper()
                    if save_format in ('JPG', 'JPEG'):
                        save_format = 'JPEG'
                        # 转换为RGB模式
                        if watermarked.mode == 'RGBA':
                            rgb_img = Image.new('RGB', watermarked.size, (255, 255, 255))
                            rgb_img.paste(watermarked, mask=watermarked.split()[-1])
                            watermarked = rgb_img
                    
                    watermarked.save(output_file, format=save_format, quality=90)
                    UIUtils.show_info("成功", f"水印图片已保存到：\n{output_file}")
                    
            except Exception as e:
                UIUtils.show_error("错误", f"保存失败：{str(e)}")
    
    def update_template_list(self):
        """更新模板列表"""
        template_names = self.template_manager.get_template_names()
        self.template_combobox['values'] = template_names
        if template_names:
            self.template_combobox.set(template_names[0])
    
    # 批量导出功能
    def export_images(self):
        """批量导出水印图片"""
        if not self.current_images:
            UIUtils.show_warning("警告", "请先导入图片文件")
            return
        
        # 选择输出目录
        output_dir = UIUtils.choose_directory(title="选择输出目录")
        if not output_dir:
            return
        
        # 创建进度对话框
        from utils.ui_utils import ProgressDialog
        progress_dialog = ProgressDialog(
            self.root,
            "批量处理",
            "正在处理图片，请稍候..."
        )
        
        def progress_callback(current, total, current_file):
            filename = os.path.basename(current_file)
            return progress_dialog.update(current, total, f"正在处理: {filename}")
        
        def text_provider(image_path):
            # 使用EXIF日期或用户输入的文本
            date_text = self.image_processor.get_date_text_for_image(
                image_path,
                self.watermark_engine.settings.get('text', 'YYYY-MM-DD')
            )
            return date_text or self.text_entry.get()
        
        try:
            # 执行批量处理
            results = self.watermark_engine.batch_apply_watermark(
                self.current_images,
                output_dir,
                text_provider=text_provider,
                progress_callback=progress_callback
            )
            
            progress_dialog.close()
            
            # 显示结果
            success_count = results['success']
            failed_count = results['failed']
            
            if failed_count == 0:
                UIUtils.show_info(
                    "完成",
                    f"批量处理完成！\n\n成功: {success_count} 张\n输出目录: {output_dir}"
                )
            else:
                error_details = "\n".join(results['errors'][:5])  # 只显示前5个错误
                if len(results['errors']) > 5:
                    error_details += f"\n...及其他 {len(results['errors']) - 5} 个错误"
                
                UIUtils.show_warning(
                    "部分失败",
                    f"批量处理完成！\n\n成功: {success_count} 张\n失败: {failed_count} 张\n\n错误详情:\n{error_details}"
                )
                
        except Exception as e:
            progress_dialog.close()
            UIUtils.show_error("错误", f"批量处理失败：{str(e)}")
    
    # 模板管理方法
    def copy_settings(self):
        """复制当前设置"""
        # TODO: 实现设置复制功能
        pass
    
    def paste_settings(self):
        """粘贴设置"""
        # TODO: 实现设置粘贴功能
        pass
    
    def new_template(self):
        """新建模板"""
        # TODO: 实现新建模板对话框
        pass
    
    def save_as_template(self):
        """将当前设置保存为模板"""
        from tkinter import simpledialog
        
        template_name = simpledialog.askstring(
            "保存模板",
            "请输入模板名称：",
            initialvalue="我的模板"
        )
        
        if template_name:
            from core.template import Template
            template = Template(template_name)
            template.update_settings(self.watermark_engine.get_settings())
            
            if self.template_manager.add_template(template):
                self.template_manager.save_templates()
                self.update_template_list()
                self.template_combobox.set(template_name)
                UIUtils.show_info("成功", f"模板 '{template_name}' 已保存")
            else:
                UIUtils.show_error("错误", f"模板名称 '{template_name}' 已存在")
    
    def manage_templates(self):
        """管理模板"""
        # TODO: 实现模板管理对话框
        pass
    
    def import_template(self):
        """导入模板"""
        template_file = UIUtils.choose_files(
            title="选择模板文件",
            filetypes=[("JSON模板", "*.json"), ("所有文件", "*.*")],
            multiple=False
        )
        
        if template_file:
            if self.template_manager.import_template(template_file[0]):
                self.template_manager.save_templates()
                self.update_template_list()
                UIUtils.show_info("成功", "模板已成功导入")
            else:
                UIUtils.show_error("错误", "导入模板失败")
    
    def export_template(self):
        """导出模板"""
        template_name = self.template_combobox.get()
        if not template_name:
            UIUtils.show_warning("警告", "请先选择一个模板")
            return
        
        output_file = UIUtils.save_file(
            title="导出模板",
            defaultextension=".json",
            filetypes=[("JSON模板", "*.json"), ("所有文件", "*.*")]
        )
        
        if output_file:
            if self.template_manager.export_template(template_name, output_file):
                UIUtils.show_info("成功", f"模板已导出到：\n{output_file}")
            else:
                UIUtils.show_error("错误", "导出模板失败")
    
    # 设置管理方法
    def load_settings(self):
        """加载应用设置"""
        try:
            # 加载窗口尺寸和位置
            geometry = self.settings_manager.get('window_geometry')
            if geometry:
                self.root.geometry(geometry)
            
            # 加载上次使用的模板
            last_template = self.settings_manager.get('last_template')
            if last_template and self.settings_manager.get('auto_load_last_template', True):
                template = self.template_manager.get_template(last_template)
                if template:
                    self.template_combobox.set(last_template)
                    self.apply_template_settings(template.settings)
                    
        except Exception as e:
            print(f"加载设置失败: {e}")
    
    def save_settings(self):
        """保存应用设置"""
        try:
            # 保存窗口尺寸和位置
            self.settings_manager.set('window_geometry', self.root.geometry())
            
            # 保存当前模板
            current_template = self.template_combobox.get()
            if current_template:
                self.settings_manager.set('last_template', current_template)
            
            self.settings_manager.save_settings()
            
        except Exception as e:
            print(f"保存设置失败: {e}")
    
    # 其他功能方法
    def show_help(self):
        """显示帮助信息"""
        help_text = """
照片水印工具 v1.0 使用说明

1. 导入图片：
   - 点击“导入图片”按钮选择单个或多个图片文件
   - 点击“导入文件夹”按钮选择包含图片的文件夹

2. 设置水印：
   - 选择预设模板或自定义设置
   - 调整水印文本、字体大小、颜色和透明度
   - 选择水印位置和边距

3. 预览和导出：
   - 在右侧预览区查看水印效果
   - 点击“应用到当前”保存单张图片
   - 点击“批量导出”处理所有图片

4. 模板管理：
   - 保存常用设置为模板
   - 导入/导出模板文件

快捷键：
- Ctrl+O: 导入图片
- Ctrl+Shift+O: 导入文件夹
- Ctrl+S: 批量导出
- F5: 刷新预览
- 左/右箭头: 切换图片
        """
        
        # 创建帮助窗口
        help_window = tk.Toplevel(self.root)
        help_window.title("使用说明")
        help_window.geometry("600x500")
        help_window.resizable(False, False)
        UIUtils.center_window(help_window, 600, 500)
        
        # 文本显示区域
        text_frame = ttk.Frame(help_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=("Arial", 10))
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_widget.insert(tk.END, help_text)
        text_widget.config(state=tk.DISABLED)
        
        # 关闭按钮
        ttk.Button(help_window, text="关闭", command=help_window.destroy).pack(pady=10)
    
    def show_about(self):
        """显示关于信息"""
        about_text = """
照片水印工具 v1.0

一个简单易用的照片水印添加工具

功能特点：
• 支持多种图片格式（JPEG, PNG, BMP, TIFF, WebP）
• 自动读取EXIF拍摄日期作为水印
• 实时预览水印效果
• 多种水印位置和样式选择
• 模板系统支持保存和重用设置
• 批量处理功能

技术支持：Python + Tkinter + Pillow
        """
        
        UIUtils.show_info("关于", about_text)
    def on_closing(self): 
        self.save_settings()
        self.root.destroy()


def main():
    """主程序入口"""
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()