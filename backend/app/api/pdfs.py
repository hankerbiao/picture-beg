import os
import traceback
import logging
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status, Form
from fastapi.responses import FileResponse, PlainTextResponse
from sqlmodel import Session, select

from app.db.database import get_session
from app.models.pdf_convert import PDFConversion, PDFConversionRead
from app.core.pdf_handler import PDFHandler
from app.core.config import AI_BASE_URL, AI_MODEL, BASE_URL, PDF_UPLOAD_DIR as UPLOAD_DIR, PDF_OUTPUT_DIR as OUTPUT_DIR

# 创建日志记录器
logger = logging.getLogger("pdfs_api")

router = APIRouter()

# 创建PDF处理器
pdf_handler = PDFHandler(UPLOAD_DIR, OUTPUT_DIR, BASE_URL, AI_BASE_URL, AI_MODEL)


@router.post("/convert", response_model=PDFConversionRead, status_code=status.HTTP_201_CREATED)
async def convert_pdf(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    session: Session = Depends(get_session)
):
    """
    上传PDF文件并转换为Word文档
    
    - **file**: 要上传的PDF文件
    - **description**: 文档描述信息
    """
    pdf_path = None
    
    # 检查文件类型
    if not file.filename.lower().endswith('.pdf'):
        logger.warning(f"拒绝非PDF文件: {file.filename}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只接受PDF文件"
        )
    
    try:
        logger.info(f"开始处理PDF文件: {file.filename}")
        
        # 检查文件大小
        file.file.seek(0, 2)  # 移动到文件末尾
        file_size = file.file.tell()  # 获取文件大小
        file.file.seek(0)  # 重置文件指针到开头
        
        logger.info(f"上传的PDF文件大小: {file_size} 字节")
        
        if file_size == 0:
            logger.warning("上传的PDF文件为空")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="上传的PDF文件为空"
            )
        
        # 保存上传的PDF文件
        pdf_path = await pdf_handler.save_pdf(file)
        logger.info(f"PDF文件已保存到: {pdf_path}")
        
        # 检查保存的文件
        if not os.path.exists(pdf_path):
            logger.error("保存PDF文件失败")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="保存PDF文件失败"
            )
            
        saved_size = os.path.getsize(pdf_path)
        logger.info(f"保存的PDF文件大小: {saved_size} 字节")
        
        if saved_size == 0:
            logger.error("保存的PDF文件为空")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="保存的PDF文件为空"
            )
        
        # 转换PDF到Word
        logger.info("开始转换PDF到Word...")
        output_path, page_count, text_content, processed_text, markdown_path = pdf_handler.convert_pdf_to_word(pdf_path,description)
        logger.info(f"转换完成，输出路径: {output_path}, 页数: {page_count}")
        
        # 检查生成的文件
        if not os.path.exists(output_path):
            logger.error("生成Word文档失败")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="生成Word文档失败"
            )
            
        output_size = os.path.getsize(output_path)
        logger.info(f"生成的Word文档大小: {output_size} 字节")
        
        # 相对路径，用于URL
        relative_path = os.path.relpath(output_path, OUTPUT_DIR)
        markdown_relative_path = os.path.relpath(markdown_path, OUTPUT_DIR) if markdown_path and os.path.exists(markdown_path) else None
        
        # 保存转换记录到数据库
        conversion = PDFConversion(
            original_filename=file.filename,
            output_filename=os.path.basename(output_path),
            file_path=relative_path,
            page_count=page_count,
            text_content=text_content,
            processed_text=processed_text,
            markdown_path=markdown_relative_path
        )
        
        session.add(conversion)
        session.commit()
        session.refresh(conversion)
        
        # 构建下载URL
        download_url = f"{BASE_URL}/api/pdfs/download/{os.path.basename(output_path)}"
        markdown_url = f"{BASE_URL}/api/pdfs/download-markdown/{os.path.basename(markdown_path)}" if markdown_relative_path else None
        logger.info(f"转换成功，下载URL: {download_url}")
        
        # 返回结果
        return {
            **conversion.dict(),
            "download_url": download_url,
            "markdown_url": markdown_url
        }
    except HTTPException as he:
        # 重新抛出HTTP异常
        if pdf_path and os.path.exists(pdf_path):
            os.remove(pdf_path)
            logger.info(f"删除临时PDF文件: {pdf_path}")
        raise he
    except Exception as e:
        # 打印详细错误信息
        logger.error(f"转换PDF时出错: {str(e)}")
        logger.error(traceback.format_exc())
        
        # 发生错误时删除临时文件
        if pdf_path and os.path.exists(pdf_path):
            os.remove(pdf_path)
            logger.info(f"删除临时PDF文件: {pdf_path}")
            
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"转换失败: {str(e)}"
        )


@router.get("/{conversion_id}/text", response_class=PlainTextResponse)
def get_conversion_text(conversion_id: int, session: Session = Depends(get_session)):
    """
    获取PDF转换的原始文本内容
    
    - **conversion_id**: 转换记录ID
    """
    conversion = session.get(PDFConversion, conversion_id)
    if not conversion:
        logger.warning(f"未找到转换记录: ID {conversion_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="转换记录不存在"
        )
    
    if not conversion.text_content:
        logger.warning(f"转换记录 {conversion_id} 没有文本内容")
        return "此PDF文件没有提取到文本内容"
    
    logger.info(f"获取转换记录 {conversion_id} 的原始文本内容")
    return conversion.text_content


@router.get("/{conversion_id}/processed_text", response_class=PlainTextResponse)
def get_conversion_processed_text(conversion_id: int, session: Session = Depends(get_session)):
    """
    获取PDF转换的AI处理后的文本内容
    
    - **conversion_id**: 转换记录ID
    """
    conversion = session.get(PDFConversion, conversion_id)
    if not conversion:
        logger.warning(f"未找到转换记录: ID {conversion_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="转换记录不存在"
        )
    
    if not conversion.processed_text:
        logger.warning(f"转换记录 {conversion_id} 没有AI处理后的文本内容")
        return "此PDF文件没有AI处理后的文本内容"
    
    logger.info(f"获取转换记录 {conversion_id} 的AI处理后的文本内容")
    return conversion.processed_text


@router.get("/{conversion_id}/text_json")
def get_conversion_text_json(conversion_id: int, session: Session = Depends(get_session)) -> Dict[str, Any]:
    """
    获取PDF转换的文本内容（JSON格式）
    
    - **conversion_id**: 转换记录ID
    """
    conversion = session.get(PDFConversion, conversion_id)
    if not conversion:
        logger.warning(f"未找到转换记录: ID {conversion_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="转换记录不存在"
        )
    
    logger.info(f"获取转换记录 {conversion_id} 的文本内容（JSON格式）")
    return {
        "id": conversion.id,
        "original_filename": conversion.original_filename,
        "page_count": conversion.page_count,
        "text_content": conversion.text_content or "此PDF文件没有提取到文本内容",
        "processed_text": conversion.processed_text or "此PDF文件没有AI处理后的文本内容"
    }


@router.get("/", response_model=List[PDFConversionRead])
def get_conversions(session: Session = Depends(get_session)):
    """
    获取所有PDF转换记录
    """
    conversions = session.exec(select(PDFConversion).order_by(PDFConversion.created_at.desc())).all()
    logger.info(f"获取转换记录列表，共 {len(conversions)} 条")
    return conversions


@router.get("/{conversion_id}", response_model=PDFConversionRead)
def get_conversion(conversion_id: int, session: Session = Depends(get_session)):
    """
    获取单个PDF转换记录
    """
    conversion = session.get(PDFConversion, conversion_id)
    if not conversion:
        logger.warning(f"未找到转换记录: ID {conversion_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="转换记录不存在"
        )
    logger.info(f"获取转换记录: ID {conversion_id}")
    
    # 构建下载URL
    download_url = f"{BASE_URL}/api/pdfs/download/{conversion.output_filename}"
    markdown_url = None
    if conversion.markdown_path:
        markdown_filename = os.path.basename(conversion.markdown_path)
        markdown_url = f"{BASE_URL}/api/pdfs/download-markdown/{markdown_filename}"
    
    return {
        **conversion.dict(),
        "download_url": download_url,
        "markdown_url": markdown_url
    }


@router.get("/download/{filename}")
def download_file(filename: str):
    """
    下载转换后的Word文档
    
    - **filename**: 要下载的文件名
    """
    file_path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(file_path):
        logger.warning(f"下载文件不存在: {filename}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件不存在"
        )
    
    file_size = os.path.getsize(file_path)
    logger.info(f"下载文件: {filename}, 大小: {file_size} 字节")
    
    if file_size == 0:
        logger.warning(f"警告: 下载的文件 {filename} 大小为0")
    
    return FileResponse(
        path=file_path, 
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )


@router.get("/download-markdown/{filename}")
def download_markdown(filename: str):
    """
    下载Markdown文件
    
    - **filename**: 要下载的Markdown文件名
    """
    file_path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(file_path):
        logger.warning(f"下载Markdown文件不存在: {filename}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件不存在"
        )
    
    file_size = os.path.getsize(file_path)
    logger.info(f"下载Markdown文件: {filename}, 大小: {file_size} 字节")
    
    if file_size == 0:
        logger.warning(f"警告: 下载的Markdown文件 {filename} 大小为0")
    
    return FileResponse(
        path=file_path, 
        filename=filename,
        media_type="text/markdown"
    )


@router.delete("/{conversion_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_conversion(conversion_id: int, session: Session = Depends(get_session)):
    """
    删除PDF转换记录
    """
    conversion = session.get(PDFConversion, conversion_id)
    if not conversion:
        logger.warning(f"删除时未找到转换记录: ID {conversion_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="转换记录不存在"
        )
    
    try:
        # 删除Word文件
        file_path = os.path.join(OUTPUT_DIR, conversion.file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"删除Word文件: {file_path}")
        
        # 删除Markdown文件
        if conversion.markdown_path:
            markdown_path = os.path.join(OUTPUT_DIR, conversion.markdown_path)
            if os.path.exists(markdown_path):
                os.remove(markdown_path)
                logger.info(f"删除Markdown文件: {markdown_path}")
        
        # 从数据库删除记录
        session.delete(conversion)
        session.commit()
        logger.info(f"删除转换记录: ID {conversion_id}")
    except Exception as e:
        logger.error(f"删除转换记录失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除转换记录失败: {str(e)}"
        ) 