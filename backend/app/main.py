import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api import images, pdfs
from app.db.database import create_db_and_tables
from app.core.config import AI_BASE_URL, AI_MODEL, PDF_UPLOAD_DIR, PDF_OUTPUT_DIR, STATIC_FILES_DIR

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("app")

# 记录AI模型配置（仅用于日志记录）
logger.info(f"AI模型配置: {AI_BASE_URL}, 模型: {AI_MODEL}")

app = FastAPI(
    title="图床服务API",
    description="为博客提供图片存储和访问服务的API，同时支持PDF转Word功能",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境中应该限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册API路由
app.include_router(images.router, prefix="/api/images", tags=["images"])
app.include_router(pdfs.router, prefix="/api/pdfs", tags=["pdfs"])

# 挂载静态文件目录
app.mount("/static/images", StaticFiles(directory=STATIC_FILES_DIR), name="images")

# 挂载PDF和Word文件目录
os.makedirs(PDF_UPLOAD_DIR, exist_ok=True)
os.makedirs(PDF_OUTPUT_DIR, exist_ok=True)
app.mount("/static/pdfs/outputs", StaticFiles(directory=PDF_OUTPUT_DIR), name="pdf_outputs")

# 挂载静态HTML文件
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.on_event("startup")
def on_startup():
    """应用启动时执行"""
    logger.info("应用启动中...")
    create_db_and_tables()
    logger.info("数据库表已创建")
    logger.info(f"静态文件目录: {STATIC_FILES_DIR}")
    logger.info(f"PDF上传目录: {PDF_UPLOAD_DIR}")
    logger.info(f"PDF输出目录: {PDF_OUTPUT_DIR}")


@app.get("/")
def read_root():
    """根路径"""
    return {"message": "欢迎使用图床服务API"} 