"""
图像处理逻辑模块
处理图像的读取、格式转换、EXIF数据等
"""
from __future__ import annotations

import datetime as _dt
import os
from typing import Optional, List
from PIL import Image
import exifread


class ImageProcessor:
    """图像处理器 - 处理图像相关的基础操作"""
    
    # 支持的图像格式
    SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".tiff", ".tif", ".bmp"}
    
    # EXIF时间字段优先级
    EXIF_CANDIDATE_TAGS = (
        "EXIF DateTimeOriginal",
        "EXIF CreateDate", 
        "Image DateTime",
    )
    
    @classmethod
    def is_image_file(cls, path: str) -> bool:
        """检查文件是否为支持的图像格式"""
        _, ext = os.path.splitext(path)
        return ext.lower() in cls.SUPPORTED_EXTENSIONS
    
    @classmethod
    def collect_image_files(cls, input_path: str, recursive: bool = False) -> List[str]:
        """收集图像文件列表"""
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"路径不存在: {input_path}")
        
        if os.path.isfile(input_path):
            return [input_path] if cls.is_image_file(input_path) else []
        
        collected: List[str] = []
        if recursive:
            for root, _, files in os.walk(input_path):
                for name in files:
                    full = os.path.join(root, name)
                    if cls.is_image_file(full):
                        collected.append(full)
        else:
            for name in os.listdir(input_path):
                full = os.path.join(input_path, name)
                if os.path.isfile(full) and cls.is_image_file(full):
                    collected.append(full)
        
        collected.sort()
        return collected
    
    @classmethod
    def read_capture_datetime(cls, image_path: str) -> Optional[_dt.datetime]:
        """从EXIF读取拍摄时间"""
        try:
            with open(image_path, "rb") as f:
                tags = exifread.process_file(f, details=False, stop_tag="EXIF DateTimeOriginal")
        except Exception:
            return None
        
        for key in cls.EXIF_CANDIDATE_TAGS:
            v = tags.get(key)
            if not v:
                continue
            parsed = cls._parse_exif_datetime(str(v))
            if parsed:
                return parsed
        return None
    
    @staticmethod
    def _parse_exif_datetime(value: str) -> Optional[_dt.datetime]:
        """解析EXIF时间格式: YYYY:MM:DD HH:MM:SS"""
        try:
            return _dt.datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
        except Exception:
            return None
    
    @classmethod
    def get_file_datetime(cls, image_path: str) -> Optional[_dt.datetime]:
        """获取文件创建/修改时间作为后备"""
        try:
            stat = os.stat(image_path)
            timestamp = getattr(stat, "st_ctime", stat.st_mtime)
            return _dt.datetime.fromtimestamp(timestamp)
        except Exception:
            return None
    
    @classmethod
    def get_date_text_for_image(
        cls, 
        image_path: str, 
        date_format: str = "YYYY-MM-DD",
        use_file_time_fallback: bool = True
    ) -> Optional[str]:
        """获取图像的日期文本（用于水印）"""
        dt = cls.read_capture_datetime(image_path)
        if dt is None and use_file_time_fallback:
            dt = cls.get_file_datetime(image_path)
        
        if dt is None:
            return None
        
        # 只保留日期部分
        dt = _dt.datetime(dt.year, dt.month, dt.day)
        return cls.format_date(dt, date_format)
    
    @staticmethod
    def format_date(dt: _dt.datetime, fmt: str) -> str:
        """格式化日期"""
        mapping = {
            "YYYY": dt.strftime("%Y"),
            "MM": dt.strftime("%m"),
            "DD": dt.strftime("%d"),
        }
        out = fmt
        for k, v in mapping.items():
            out = out.replace(k, v)
        return out
    
    @staticmethod
    def load_image(image_path: str) -> Image.Image:
        """加载图像"""
        return Image.open(image_path)
    
    @staticmethod
    def save_image(image: Image.Image, output_path: str, format: str = None, quality: int = 90):
        """保存图像"""
        save_kwargs = {}
        if format:
            save_kwargs["format"] = format.upper()
        if format and format.lower() in ("jpeg", "jpg", "webp"):
            save_kwargs["quality"] = quality
        image.save(output_path, **save_kwargs)