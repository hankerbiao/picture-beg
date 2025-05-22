import os
from typing import List
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status, Form
from sqlmodel import Session, select

from app.db.database import get_session
from app.models.image import Image, ImageRead
from app.core.image_handler import ImageHandler

router = APIRouter()

# 从环境变量获取配置
STATIC_FILES_DIR = os.getenv("STATIC_FILES_DIR", "app/static/images")
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

# 创建图片处理器
image_handler = ImageHandler(STATIC_FILES_DIR, BASE_URL)


@router.post("/upload", response_model=ImageRead, status_code=status.HTTP_201_CREATED)
async def upload_image(
    file: UploadFile = File(...),
    description: str = Form(None),
    session: Session = Depends(get_session)
):
    """
    上传图片API
    """
    # 验证是否为图片文件
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只允许上传图片文件"
        )
    
    try:
        # 保存图片
        image_data = await image_handler.save_image(file)
        
        # 添加描述
        if description:
            image_data["description"] = description
        
        # 保存到数据库
        image = Image(**image_data)
        session.add(image)
        session.commit()
        session.refresh(image)
        
        return image
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"上传图片失败: {str(e)}"
        )


@router.get("/", response_model=List[ImageRead])
def get_images(session: Session = Depends(get_session)):
    """
    获取所有图片
    """
    images = session.exec(select(Image).order_by(Image.created_at.desc())).all()
    return images


@router.get("/{image_id}", response_model=ImageRead)
def get_image(image_id: int, session: Session = Depends(get_session)):
    """
    获取单张图片信息
    """
    image = session.get(Image, image_id)
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="图片不存在"
        )
    return image


@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_image(image_id: int, session: Session = Depends(get_session)):
    """
    删除图片
    """
    image = session.get(Image, image_id)
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="图片不存在"
        )
    
    try:
        # 删除文件
        file_path = os.path.join(STATIC_FILES_DIR, image.file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # 从数据库删除记录
        session.delete(image)
        session.commit()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除图片失败: {str(e)}"
        ) 