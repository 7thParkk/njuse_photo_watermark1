"""
文件工具 - 处理文件相关操作
"""
from __future__ import annotations

import os
import shutil
from typing import List, Optional, Tuple
from PIL import Image


class FileUtils:
    """文件处理工具类"""
    
    @staticmethod
    def ensure_output_dir(input_path: str, suffix: str = "_watermark") -> str:
        """确保输出目录存在"""
        if os.path.isfile(input_path):
            parent = os.path.dirname(input_path)
            base_dir = os.path.basename(parent)
            out_dir = os.path.join(parent, f"{base_dir}{suffix}")
        else:
            parent = input_path
            base_dir = os.path.basename(os.path.normpath(input_path))
            out_dir = os.path.join(parent, f"{base_dir}{suffix}")
        
        os.makedirs(out_dir, exist_ok=True)
        return out_dir
    
    @staticmethod
    def get_output_path(
        input_file: str,
        output_dir: str,
        suffix: str = "_wm",
        ext: Optional[str] = None,
        overwrite: bool = False
    ) -> str:
        """生成输出文件路径"""
        name, original_ext = os.path.splitext(os.path.basename(input_file))
        out_ext = (ext or original_ext.lstrip(".")).lower()
        if not out_ext.startswith("."):
            out_ext = "." + out_ext
        
        candidate = os.path.join(output_dir, f"{name}{suffix}{out_ext}")
        if overwrite or not os.path.exists(candidate):
            return candidate
        
        # 递增命名避免冲突
        index = 1
        while True:
            cand = os.path.join(output_dir, f"{name}{suffix} ({index}){out_ext}")
            if not os.path.exists(cand):
                return cand
            index += 1
    
    @staticmethod
    def get_safe_filename(filename: str) -> str:
        """获取安全的文件名（移除不安全字符）"""
        import re
        # 移除或替换不安全的字符
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # 移除多余的空格和点
        safe_name = re.sub(r'\s+', ' ', safe_name).strip('. ')
        return safe_name
    
    @staticmethod
    def get_file_size_str(file_path: str) -> str:
        """获取文件大小的字符串表示"""
        try:
            size = os.path.getsize(file_path)
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024:
                    return f"{size:.1f} {unit}"
                size /= 1024
            return f"{size:.1f} TB"
        except:
            return "未知"
    
    @staticmethod
    def create_thumbnail(image_path: str, size: Tuple[int, int] = (200, 150)) -> Optional[Image.Image]:
        """创建缩略图"""
        try:
            with Image.open(image_path) as img:
                # 创建缩略图副本
                img_copy = img.copy()
                img_copy.thumbnail(size, Image.Resampling.LANCZOS)
                return img_copy
        except Exception:
            return None
    
    @staticmethod
    def validate_image_file(file_path: str) -> Tuple[bool, str]:
        """验证图像文件"""
        if not os.path.exists(file_path):
            return False, "文件不存在"
        
        if not os.path.isfile(file_path):
            return False, "不是文件"
        
        try:
            with Image.open(file_path) as img:
                img.verify()  # 验证图像完整性
            return True, "有效"
        except Exception as e:
            return False, f"无效图像: {str(e)}"
    
    @staticmethod
    def get_image_info(image_path: str) -> dict:
        """获取图像信息"""
        info = {
            'path': image_path,
            'name': os.path.basename(image_path),
            'size': FileUtils.get_file_size_str(image_path),
            'valid': False,
            'width': 0,
            'height': 0,
            'format': 'Unknown',
            'mode': 'Unknown'
        }
        
        try:
            with Image.open(image_path) as img:
                info.update({
                    'valid': True,
                    'width': img.width,
                    'height': img.height,
                    'format': img.format or 'Unknown',
                    'mode': img.mode
                })
        except Exception:
            pass
        
        return info
    
    @staticmethod
    def backup_file(file_path: str, backup_dir: str = None) -> Optional[str]:
        """备份文件"""
        if not os.path.exists(file_path):
            return None
        
        if backup_dir is None:
            backup_dir = os.path.join(os.path.dirname(file_path), 'backup')
        
        os.makedirs(backup_dir, exist_ok=True)
        
        filename = os.path.basename(file_path)
        name, ext = os.path.splitext(filename)
        
        # 生成备份文件名
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"{name}_backup_{timestamp}{ext}"
        backup_path = os.path.join(backup_dir, backup_filename)
        
        try:
            shutil.copy2(file_path, backup_path)
            return backup_path
        except Exception:
            return None


class ImageCache:
    """图像缓存管理"""
    
    def __init__(self, max_size: int = 50):
        self.max_size = max_size
        self.cache = {}
        self.access_order = []
    
    def get(self, key: str) -> Optional[Image.Image]:
        """获取缓存的图像"""
        if key in self.cache:
            # 更新访问顺序
            self.access_order.remove(key)
            self.access_order.append(key)
            return self.cache[key].copy()
        return None
    
    def put(self, key: str, image: Image.Image):
        """放入缓存"""
        # 如果已存在，更新
        if key in self.cache:
            self.cache[key] = image.copy()
            self.access_order.remove(key)
            self.access_order.append(key)
            return
        
        # 检查缓存大小
        while len(self.cache) >= self.max_size:
            # 移除最久未访问的项
            oldest = self.access_order.pop(0)
            del self.cache[oldest]
        
        # 添加新项
        self.cache[key] = image.copy()
        self.access_order.append(key)
    
    def clear(self):
        """清空缓存"""
        self.cache.clear()
        self.access_order.clear()
    
    def remove(self, key: str):
        """移除指定项"""
        if key in self.cache:
            del self.cache[key]
            self.access_order.remove(key)