"""
水印引擎 - 核心水印处理逻辑
支持实时预览和批量处理两种模式
"""
from __future__ import annotations

import math
from typing import Tuple, Optional, Union
from PIL import Image, ImageDraw, ImageFont
from PIL.ImageFont import FreeTypeFont, ImageFont as PILImageFont


class WatermarkEngine:
    """水印引擎 - 处理所有水印相关的操作"""
    
    # 预设位置映射
    POSITION_MAP = {
        "top-left": "top_left",
        "top-center": "top_center", 
        "top-right": "top_right",
        "center-left": "center_left",
        "center": "center",
        "center-right": "center_right",
        "bottom-left": "bottom_left",
        "bottom-center": "bottom_center",
        "bottom-right": "bottom_right"
    }
    
    def __init__(self):
        self.settings = {
            'text': '',
            'font_path': None,
            'font_size': 32,
            'color': '#FFFFFF',
            'transparency': 100,  # 0-100%
            'position': 'bottom-right',
            'custom_x': 0,
            'custom_y': 0, 
            'margin_x': 16,
            'margin_y': 16,
            'rotation': 0,  # 旋转角度
            'shadow_enabled': True,
            'shadow_offset': 1,
            'shadow_color': '#000000',
            'shadow_transparency': 50,
            'stroke_enabled': False,
            'stroke_width': 2,
            'stroke_color': '#000000'
        }
    
    def update_settings(self, **kwargs):
        """更新水印设置"""
        for key, value in kwargs.items():
            if key in self.settings:
                self.settings[key] = value
    
    def get_settings(self) -> dict:
        """获取当前设置"""
        return self.settings.copy()
    
    def load_font(self, font_path: Optional[str], font_size: int) -> Union[FreeTypeFont, PILImageFont]:
        """加载字体"""
        try:
            if font_path and font_path.strip():
                return ImageFont.truetype(font_path, font_size)
        except Exception:
            pass
        
        # 回退到默认字体
        try:
            return ImageFont.load_default()
        except Exception:
            return ImageFont.load_default()
    
    def measure_text(self, draw: ImageDraw.ImageDraw, text: str, font: Union[FreeTypeFont, PILImageFont]) -> Tuple[int, int]:
        """测量文本尺寸"""
        bbox = draw.textbbox((0, 0), text, font=font)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        return width, height
    
    def compute_position(
        self, 
        image_size: Tuple[int, int], 
        text_size: Tuple[int, int], 
        position: str = None,
        custom_x: int = None,
        custom_y: int = None,
        margin_x: int = 16,
        margin_y: int = 16
    ) -> Tuple[int, int]:
        """计算水印位置"""
        img_w, img_h = image_size
        txt_w, txt_h = text_size
        
        # 如果指定了自定义坐标，直接使用
        if custom_x is not None and custom_y is not None:
            return max(0, min(custom_x, img_w - txt_w)), max(0, min(custom_y, img_h - txt_h))
        
        # 使用预设位置
        pos = (position or self.settings['position']).lower().replace('-', '_')
        
        if pos == "top_left":
            return margin_x, margin_y
        elif pos == "top_center":
            return (img_w - txt_w) // 2, margin_y
        elif pos == "top_right":
            return max(margin_x, img_w - txt_w - margin_x), margin_y
        elif pos == "center_left":
            return margin_x, (img_h - txt_h) // 2
        elif pos == "center":
            return (img_w - txt_w) // 2, (img_h - txt_h) // 2
        elif pos == "center_right":
            return max(margin_x, img_w - txt_w - margin_x), (img_h - txt_h) // 2
        elif pos == "bottom_left":
            return margin_x, max(margin_y, img_h - txt_h - margin_y)
        elif pos == "bottom_center":
            return (img_w - txt_w) // 2, max(margin_y, img_h - txt_h - margin_y)
        else:  # bottom_right (默认)
            return max(margin_x, img_w - txt_w - margin_x), max(margin_y, img_h - txt_h - margin_y)
    
    def apply_watermark(
        self, 
        image: Image.Image, 
        text: str = None,
        preview_mode: bool = False,
        **override_settings
    ) -> Image.Image:
        """
        应用水印到图像
        
        Args:
            image: 源图像
            text: 水印文本（如果不提供则使用设置中的文本）
            preview_mode: 预览模式（使用较低质量以提高性能）
            **override_settings: 临时覆盖的设置
        
        Returns:
            带水印的图像
        """
        # 合并设置
        current_settings = self.settings.copy()
        current_settings.update(override_settings)
        
        # 使用提供的文本或设置中的文本
        watermark_text = text or current_settings['text']
        if not watermark_text:
            return image.copy()
        
        # 确保图像是RGBA模式以支持透明度
        if image.mode not in ("RGB", "RGBA"):
            work_image = image.convert("RGBA")
        else:
            work_image = image.copy()
        
        # 预览模式优化：缩小图像尺寸
        original_image = work_image
        if preview_mode and (work_image.width > 800 or work_image.height > 600):
            # 计算缩放比例
            scale = min(800 / work_image.width, 600 / work_image.height)
            new_size = (int(work_image.width * scale), int(work_image.height * scale))
            work_image = work_image.resize(new_size, Image.Resampling.LANCZOS)
            # 同时调整字体大小和边距
            current_settings = current_settings.copy()
            current_settings['font_size'] = int(current_settings['font_size'] * scale)
            current_settings['margin_x'] = int(current_settings['margin_x'] * scale)
            current_settings['margin_y'] = int(current_settings['margin_y'] * scale)
        
        # 加载字体
        font = self.load_font(current_settings['font_path'], current_settings['font_size'])
        draw = ImageDraw.Draw(work_image)
        
        # 计算文本尺寸和位置
        text_w, text_h = self.measure_text(draw, watermark_text, font)
        
        # 处理旋转
        rotation = current_settings.get('rotation', 0)
        if rotation != 0:
            # 计算旋转后的边界框
            rad = math.radians(rotation)
            cos_a, sin_a = abs(math.cos(rad)), abs(math.sin(rad))
            rotated_w = int(text_w * cos_a + text_h * sin_a)
            rotated_h = int(text_w * sin_a + text_h * cos_a)
            text_w, text_h = rotated_w, rotated_h
        
        # 计算位置
        x, y = self.compute_position(
            work_image.size,
            (text_w, text_h),
            current_settings['position'],
            current_settings.get('custom_x'),
            current_settings.get('custom_y'),
            current_settings['margin_x'],
            current_settings['margin_y']
        )
        
        # 处理颜色和透明度
        color = current_settings['color']
        transparency = current_settings['transparency']
        if transparency < 100:
            alpha = int(255 * transparency / 100)
            if color.startswith('#'):
                # 转换十六进制颜色为RGBA
                color = color.lstrip('#')
                rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
                color = rgb + (alpha,)
        
        # 绘制阴影（如果启用）
        if current_settings.get('shadow_enabled', False):
            shadow_offset = current_settings.get('shadow_offset', 1)
            shadow_color = current_settings.get('shadow_color', '#000000')
            shadow_transparency = current_settings.get('shadow_transparency', 50)
            
            shadow_alpha = int(255 * shadow_transparency / 100)
            if shadow_color.startswith('#'):
                shadow_color = shadow_color.lstrip('#')
                shadow_rgb = tuple(int(shadow_color[i:i+2], 16) for i in (0, 2, 4))
                shadow_color = shadow_rgb + (shadow_alpha,)
            
            shadow_x = x + shadow_offset
            shadow_y = y + shadow_offset
            
            if rotation != 0:
                # 旋转文本需要特殊处理
                self._draw_rotated_text(
                    draw, watermark_text, (shadow_x, shadow_y), font, 
                    shadow_color, rotation
                )
            else:
                draw.text((shadow_x, shadow_y), watermark_text, fill=shadow_color, font=font)
        
        # 绘制描边（如果启用）
        if current_settings.get('stroke_enabled', False):
            stroke_width = current_settings.get('stroke_width', 2)
            stroke_color = current_settings.get('stroke_color', '#000000')
            
            if rotation != 0:
                # 旋转文本的描边处理
                for dx in range(-stroke_width, stroke_width + 1):
                    for dy in range(-stroke_width, stroke_width + 1):
                        if dx == 0 and dy == 0:
                            continue
                        self._draw_rotated_text(
                            draw, watermark_text, (x + dx, y + dy), font,
                            stroke_color, rotation
                        )
            else:
                # 普通描边
                for dx in range(-stroke_width, stroke_width + 1):
                    for dy in range(-stroke_width, stroke_width + 1):
                        if dx == 0 and dy == 0:
                            continue
                        draw.text((x + dx, y + dy), watermark_text, fill=stroke_color, font=font)
        
        # 绘制主文本
        if rotation != 0:
            self._draw_rotated_text(draw, watermark_text, (x, y), font, color, rotation)
        else:
            draw.text((x, y), watermark_text, fill=color, font=font)
        
        # 预览模式需要将结果缩放回原始大小
        if preview_mode and work_image.size != original_image.size:
            work_image = work_image.resize(original_image.size, Image.Resampling.LANCZOS)
        
        return work_image
    
    def _draw_rotated_text(
        self, 
        draw: ImageDraw.ImageDraw, 
        text: str, 
        position: Tuple[int, int], 
        font: Union[FreeTypeFont, PILImageFont],
        color: Union[str, Tuple],
        rotation: float
    ):
        """绘制旋转文本"""
        x, y = position
        
        # 创建临时图像来绘制文本
        text_w, text_h = self.measure_text(draw, text, font)
        
        # 创建足够大的临时图像
        temp_size = max(text_w, text_h) * 2
        temp_img = Image.new('RGBA', (temp_size, temp_size), (0, 0, 0, 0))
        temp_draw = ImageDraw.Draw(temp_img)
        
        # 在临时图像中心绘制文本
        temp_x = (temp_size - text_w) // 2
        temp_y = (temp_size - text_h) // 2
        temp_draw.text((temp_x, temp_y), text, fill=color, font=font)
        
        # 旋转临时图像
        rotated = temp_img.rotate(rotation, expand=True)
        
        # 计算粘贴位置
        paste_x = x - rotated.width // 2
        paste_y = y - rotated.height // 2
        
        # 将旋转后的文本粘贴到主图像
        if rotated.mode == 'RGBA':
            draw._image.paste(rotated, (paste_x, paste_y), rotated)
        else:
            draw._image.paste(rotated, (paste_x, paste_y))
    
    def batch_apply_watermark(
        self, 
        image_paths: list, 
        output_dir: str,
        text_provider: callable = None,
        progress_callback: callable = None
    ) -> dict:
        """
        批量应用水印
        
        Args:
            image_paths: 图像文件路径列表
            output_dir: 输出目录
            text_provider: 文本提供器函数 (image_path) -> text
            progress_callback: 进度回调函数 (current, total, current_file)
        
        Returns:
            处理结果统计 {'success': int, 'failed': int, 'errors': list}
        """
        import os
        
        results = {'success': 0, 'failed': 0, 'errors': []}
        total = len(image_paths)
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        for i, image_path in enumerate(image_paths):
            try:
                if progress_callback:
                    progress_callback(i + 1, total, image_path)
                
                # 获取水印文本
                watermark_text = self.settings['text']
                if text_provider:
                    custom_text = text_provider(image_path)
                    if custom_text:
                        watermark_text = custom_text
                
                # 加载图像
                with Image.open(image_path) as img:
                    # 应用水印
                    watermarked = self.apply_watermark(img, watermark_text)
                    
                    # 生成输出路径
                    filename = os.path.basename(image_path)
                    name, ext = os.path.splitext(filename)
                    output_path = os.path.join(output_dir, f"{name}_watermarked{ext}")
                    
                    # 避免文件名冲突
                    counter = 1
                    while os.path.exists(output_path):
                        output_path = os.path.join(output_dir, f"{name}_watermarked_{counter}{ext}")
                        counter += 1
                    
                    # 保存图像
                    save_format = ext.lstrip('.').upper()
                    if save_format in ('JPG', 'JPEG'):
                        save_format = 'JPEG'
                        # 转换为RGB模式以支持JPEG
                        if watermarked.mode == 'RGBA':
                            rgb_img = Image.new('RGB', watermarked.size, (255, 255, 255))
                            rgb_img.paste(watermarked, mask=watermarked.split()[-1])
                            watermarked = rgb_img
                    
                    watermarked.save(output_path, format=save_format, quality=90)
                    results['success'] += 1
                    
            except Exception as e:
                results['failed'] += 1
                results['errors'].append(f"{image_path}: {str(e)}")
        
        return results