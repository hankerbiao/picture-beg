from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, Text


class PDFConversionBase(SQLModel):
    """PDF转换基本信息模型"""
    original_filename: str
    output_filename: str
    file_path: str
    page_count: int
    text_content: Optional[str] = Field(default=None, sa_column=Column(Text))
    processed_text: Optional[str] = Field(default=None, sa_column=Column(Text))
    markdown_path: Optional[str] = None


class PDFConversion(PDFConversionBase, table=True):
    """PDF转换数据表模型"""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)


class PDFConversionCreate(PDFConversionBase):
    """PDF转换创建模型"""
    pass


class PDFConversionRead(PDFConversionBase):
    """PDF转换读取模型"""
    id: int
    created_at: datetime
    download_url: Optional[str] = None
    markdown_url: Optional[str] = None 