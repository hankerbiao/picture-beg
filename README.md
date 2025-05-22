# 博客图床服务

这是一个简单的图床服务应用，用于存储和管理博客图片。

## 功能特点

- 图片上传：支持拖拽和点击上传
- 图片浏览：展示已上传图片的缩略图和信息
- 图片管理：复制URL，删除图片
- 响应式设计：适配不同屏幕尺寸

## 技术栈

### 前端
- React 18
- Ant Design 5
- Tailwind CSS
- TypeScript
- Vite

### 后端
- FastAPI
- SQLModel + MySQL
- Python 3.9+

## 本地开发

### 后端设置

1. 创建虚拟环境并安装依赖：

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. 创建`.env`文件（基于`env.example`）并配置数据库连接：

```
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/image_hosting
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
STATIC_FILES_DIR=app/static/images
BASE_URL=http://localhost:8000
```

3. 启动后端服务：

```bash
python run.py
```

### 前端设置

1. 安装依赖：

```bash
cd frontend
pnpm install
```

2. 启动开发服务器：

```bash
pnpm dev
```

## 部署

### 后端

1. 在服务器上安装依赖
2. 根据需要配置环境变量
3. 使用uvicorn或gunicorn运行FastAPI应用

### 前端

1. 构建生产版本：

```bash
pnpm build
```

2. 将`dist`目录中生成的静态文件部署到Web服务器 