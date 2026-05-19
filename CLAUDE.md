# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

这是一个博客图床服务应用，同时支持PDF转Word功能。

## Commands

### Backend (FastAPI)
```bash
cd backend
# 启动服务
python run.py
```

### Frontend (React + Vite)
```bash
cd frontend
pnpm dev      # 开发服务器
pnpm build    # 生产构建
```

### Clipboard Monitor Tool
```bash
python clipboard_monitor.py
```

## Architecture

### Backend (`backend/app/`)
- `api/` - FastAPI路由 (images.py, pdfs.py)
- `core/` - 业务处理器 (image_handler.py, pdf_handler.py, ai_processor.py)
- `db/` - 数据库配置 (SQLModel + MySQL)
- `models/` - 数据模型 (Image, PDFConversion)

### Frontend (`frontend/src/`)
- `pages/` - 页面组件 (HomePage.tsx)
- `components/` - UI组件 (UploadImage, ImageList)
- `services/` - API调用 (api.ts)
- `types/` - TypeScript类型定义

### Clipboard Monitor
独立工具 `clipboard_monitor.py` - 监控剪贴板图片并自动上传到服务器

## Configuration

### Environment Variables (backend/.env)
```
DATABASE_URL=mysql+pymysql://user:password@host:3306/dbname
AI_BASE_URL=http://xxx:18084/v1
AI_MODEL=Qwen3-32B
PDF_UPLOAD_DIR=app/static/pdfs/uploads
PDF_OUTPUT_DIR=app/static/pdfs/outputs
STATIC_FILES_DIR=app/static/images
BASE_URL=http://localhost:8000
```

## Tech Stack

- **Backend**: FastAPI, SQLModel, MySQL (pymysql), Python 3.12+
- **Frontend**: React 18, Ant Design 5, Tailwind CSS 4, TypeScript, Vite
- **Database**: MySQL (remote: 10.17.48.246:3306/nettrix_dev)