"""
模板系统 - 水印设置模板的保存和管理
"""
from __future__ import annotations

import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime


class Template:
    """水印设置模板"""
    
    def __init__(self, name: str = "新模板"):
        self.name = name
        self.created_time = datetime.now()
        self.modified_time = datetime.now()
        
        # 水印设置
        self.settings = {
            'text': '',
            'font_path': None,
            'font_size': 32,
            'color': '#FFFFFF',
            'transparency': 100,
            'position': 'bottom-right',
            'custom_x': None,
            'custom_y': None,
            'margin_x': 16,
            'margin_y': 16,
            'rotation': 0,
            'shadow_enabled': True,
            'shadow_offset': 1,
            'shadow_color': '#000000',
            'shadow_transparency': 50,
            'stroke_enabled': False,
            'stroke_width': 2,
            'stroke_color': '#000000'
        }
    
    def update_settings(self, settings: Dict[str, Any]):
        """更新模板设置"""
        self.settings.update(settings)
        self.modified_time = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式用于序列化"""
        return {
            'name': self.name,
            'created_time': self.created_time.isoformat(),
            'modified_time': self.modified_time.isoformat(),
            'settings': self.settings
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Template':
        """从字典创建模板对象"""
        template = cls(data.get('name', '新模板'))
        
        if 'created_time' in data:
            template.created_time = datetime.fromisoformat(data['created_time'])
        if 'modified_time' in data:
            template.modified_time = datetime.fromisoformat(data['modified_time'])
        if 'settings' in data:
            template.settings.update(data['settings'])
        
        return template
    
    def copy(self, new_name: str = None) -> 'Template':
        """复制模板"""
        new_template = Template(new_name or f"{self.name} - 副本")
        new_template.settings = self.settings.copy()
        return new_template


class TemplateManager:
    """模板管理器"""
    
    def __init__(self, templates_dir: str = None):
        # 默认模板目录
        if templates_dir is None:
            templates_dir = os.path.join(os.path.expanduser('~'), '.photo_watermark', 'templates')
        
        self.templates_dir = templates_dir
        self.templates_file = os.path.join(templates_dir, 'templates.json')
        self.templates: Dict[str, Template] = {}
        
        # 确保模板目录存在
        os.makedirs(templates_dir, exist_ok=True)
        
        # 加载现有模板
        self.load_templates()
        
        # 创建默认模板（如果没有模板）
        if not self.templates:
            self._create_default_templates()
    
    def _create_default_templates(self):
        """创建默认模板"""
        # 简约白色水印
        simple_white = Template("简约白色")
        simple_white.settings.update({
            'text': 'YYYY-MM-DD',
            'font_size': 32,
            'color': '#FFFFFF',
            'position': 'bottom-right',
            'shadow_enabled': True,
            'shadow_offset': 1
        })
        
        # 优雅黑色水印
        elegant_black = Template("优雅黑色")
        elegant_black.settings.update({
            'text': 'YYYY-MM-DD',
            'font_size': 28,
            'color': '#000000',
            'position': 'bottom-left',
            'shadow_enabled': False,
            'stroke_enabled': True,
            'stroke_width': 1,
            'stroke_color': '#FFFFFF'
        })
        
        # 中心大字体
        center_large = Template("中心大字体")
        center_large.settings.update({
            'text': 'YYYY-MM-DD',
            'font_size': 48,
            'color': '#FFFFFF',
            'position': 'center',
            'transparency': 70,
            'shadow_enabled': True,
            'shadow_offset': 2
        })
        
        # 保存默认模板
        self.add_template(simple_white)
        self.add_template(elegant_black)
        self.add_template(center_large)
        self.save_templates()
    
    def add_template(self, template: Template) -> bool:
        """添加模板"""
        if template.name in self.templates:
            return False  # 模板名已存在
        
        self.templates[template.name] = template
        return True
    
    def remove_template(self, name: str) -> bool:
        """删除模板"""
        if name in self.templates:
            del self.templates[name]
            return True
        return False
    
    def get_template(self, name: str) -> Optional[Template]:
        """获取模板"""
        return self.templates.get(name)
    
    def get_template_names(self) -> List[str]:
        """获取所有模板名称"""
        return list(self.templates.keys())
    
    def rename_template(self, old_name: str, new_name: str) -> bool:
        """重命名模板"""
        if old_name not in self.templates or new_name in self.templates:
            return False
        
        template = self.templates[old_name]
        template.name = new_name
        template.modified_time = datetime.now()
        
        self.templates[new_name] = template
        del self.templates[old_name]
        
        return True
    
    def duplicate_template(self, name: str, new_name: str) -> bool:
        """复制模板"""
        if name not in self.templates or new_name in self.templates:
            return False
        
        original = self.templates[name]
        duplicate = original.copy(new_name)
        self.templates[new_name] = duplicate
        
        return True
    
    def load_templates(self):
        """从文件加载模板"""
        try:
            if os.path.exists(self.templates_file):
                with open(self.templates_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                for template_data in data.get('templates', []):
                    template = Template.from_dict(template_data)
                    self.templates[template.name] = template
                    
        except Exception as e:
            print(f"加载模板失败: {e}")
    
    def save_templates(self):
        """保存模板到文件"""
        try:
            data = {
                'version': '1.0',
                'saved_time': datetime.now().isoformat(),
                'templates': [template.to_dict() for template in self.templates.values()]
            }
            
            with open(self.templates_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"保存模板失败: {e}")
    
    def export_template(self, name: str, file_path: str) -> bool:
        """导出单个模板到文件"""
        if name not in self.templates:
            return False
        
        try:
            template = self.templates[name]
            data = {
                'version': '1.0',
                'exported_time': datetime.now().isoformat(),
                'template': template.to_dict()
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception:
            return False
    
    def import_template(self, file_path: str, overwrite: bool = False) -> bool:
        """从文件导入模板"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            template_data = data.get('template')
            if not template_data:
                return False
            
            template = Template.from_dict(template_data)
            
            # 检查名称冲突
            original_name = template.name
            counter = 1
            while template.name in self.templates:
                if overwrite:
                    break
                template.name = f"{original_name} ({counter})"
                counter += 1
            
            self.templates[template.name] = template
            return True
            
        except Exception:
            return False
    
    def get_recent_templates(self, limit: int = 5) -> List[Template]:
        """获取最近使用的模板"""
        sorted_templates = sorted(
            self.templates.values(),
            key=lambda t: t.modified_time,
            reverse=True
        )
        return sorted_templates[:limit]


class SettingsManager:
    """应用设置管理器"""
    
    def __init__(self, settings_dir: str = None):
        if settings_dir is None:
            settings_dir = os.path.join(os.path.expanduser('~'), '.photo_watermark')
        
        self.settings_dir = settings_dir
        self.settings_file = os.path.join(settings_dir, 'settings.json')
        
        # 默认设置
        self.settings = {
            'window_geometry': '1200x800+100+100',
            'last_template': None,
            'last_input_dir': '',
            'last_output_dir': '',
            'auto_load_last_template': True,
            'preview_quality': 'medium',  # low, medium, high
            'default_output_format': 'same',  # same, jpg, png
            'default_output_quality': 90,
            'show_tips': True,
            'language': 'zh_CN'
        }
        
        os.makedirs(settings_dir, exist_ok=True)
        self.load_settings()
    
    def get(self, key: str, default=None):
        """获取设置值"""
        return self.settings.get(key, default)
    
    def set(self, key: str, value):
        """设置值"""
        self.settings[key] = value
    
    def load_settings(self):
        """加载设置"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    saved_settings = json.load(f)
                    self.settings.update(saved_settings)
        except Exception as e:
            print(f"加载设置失败: {e}")
    
    def save_settings(self):
        """保存设置"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存设置失败: {e}")