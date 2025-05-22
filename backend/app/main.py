import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from app.api import images
from app.db.database import create_db_and_tables

load_dotenv()

app = FastAPI(
    title="图床服务API",
    description="为博客提供图片存储和访问服务的API",
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

# 挂载静态文件目录
STATIC_FILES_DIR = os.getenv("STATIC_FILES_DIR", "app/static/images")
app.mount("/static/images", StaticFiles(directory=STATIC_FILES_DIR), name="images")


@app.on_event("startup")
def on_startup():
    """应用启动时执行"""
    create_db_and_tables()


@app.get("/")
def read_root():
    """根路径"""
    return {"message": "欢迎使用图床服务API"} 