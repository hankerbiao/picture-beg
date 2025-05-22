import os
import uuid
from fastapi import UploadFile
import shutil
from datetime import datetime


class ImageHandler:
    """图片处理工具类"""
    
    def __init__(self, static_dir: str, base_url: str):
        self.static_dir = static_dir
        self.base_url = base_url
        os.makedirs(static_dir, exist_ok=True)
    
    async def save_image(self, file: UploadFile) -> dict:
        """
        保存上传的图片文件
        
        Args:
            file: 上传的图片文件
            
        Returns:
            包含图片信息的字典
        """
        # 获取文件扩展名
        content_type = file.content_type
        ext = self._get_extension_from_content_type(content_type)
        
        # 生成唯一文件名
        filename = f"{uuid.uuid4()}{ext}"
        year_month = datetime.now().strftime("%Y%m")
        
        # 创建年月目录
        dir_path = os.path.join(self.static_dir, year_month)
        os.makedirs(dir_path, exist_ok=True)
        
        # 文件保存路径
        file_path = os.path.join(dir_path, filename)
        
        # 保存文件
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 计算相对路径供URL使用
        relative_path = os.path.join(year_month, filename)
        url = f"{self.base_url}/static/images/{relative_path}"
        
        # 获取文件大小
        size = os.path.getsize(file_path)
        
        return {
            "original_filename": file.filename,
            "file_path": relative_path,
            "url": url,
            "size": size,
            "content_type": content_type
        }
    
    @staticmethod
    def _get_extension_from_content_type(content_type: str) -> str:
        """从MIME类型获取文件扩展名"""
        content_type_map = {
            "image/jpeg": ".jpg",
            "image/png": ".png",
            "image/gif": ".gif",
            "image/webp": ".webp",
            "image/svg+xml": ".svg",
        }
        return content_type_map.get(content_type, ".jpg") 