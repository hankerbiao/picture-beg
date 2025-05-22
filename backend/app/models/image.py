from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class ImageBase(SQLModel):
    """图片基本信息模型"""
    original_filename: str
    file_path: str
    url: str
    size: int
    content_type: str
    description: Optional[str] = None


class Image(ImageBase, table=True):
    """图片数据表模型"""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)


class ImageCreate(ImageBase):
    """图片创建模型"""
    pass


class ImageRead(ImageBase):
    """图片读取模型"""
    id: int
    created_at: datetime 