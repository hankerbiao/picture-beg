import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# AI相关配置
AI_BASE_URL = os.getenv("AI_BASE_URL", "http://123.157.247.187:18084/v1")
AI_MODEL = os.getenv("AI_MODEL", "Qwen3-32B")

# PDF相关配置
PDF_UPLOAD_DIR = os.getenv("PDF_UPLOAD_DIR", "app/static/pdfs/uploads")
PDF_OUTPUT_DIR = os.getenv("PDF_OUTPUT_DIR", "app/static/pdfs/outputs")

# 基础URL配置
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

# 静态文件目录
STATIC_FILES_DIR = os.getenv("STATIC_FILES_DIR", "app/static/images") 