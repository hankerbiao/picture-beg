# 博客图床服务

这是一个博客图床服务应用，提供图片上传、管理功能。

## 功能特点

- 图片上传：支持拖拽和点击上传
- 图片浏览：展示已上传图片的缩略图和信息
- 图片管理：复制URL，删除图片
- 响应式设计：适配不同屏幕尺寸
- 剪贴板监控：一键截屏上传

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
- Python 3.12+

## 本地开发

### 后端设置

1. 创建虚拟环境并安装依赖：

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. 创建`.env`文件并配置数据库连接：

```bash
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/image_hosting
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

## API 文档

启动后端服务后，访问 http://localhost:8000/docs 查看完整的 Swagger API 文档。

### 图片 API

#### 上传图片

```bash
curl -X POST "http://localhost:8000/api/images/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/image.png" \
  -F "description=图片描述（可选）"
```

**响应示例：**

```json
{
  "id": 1,
  "original_filename": "image.png",
  "file_path": "2025/01/19/abc123.png",
  "url": "http://localhost:8000/static/images/2025/01/19/abc123.png",
  "size": 102400,
  "content_type": "image/png",
  "description": "图片描述",
  "created_at": "2025-01-19T10:30:00"
}
```

#### 获取所有图片

```bash
curl -X GET "http://localhost:8000/api/images"
```

#### 获取单张图片

```bash
curl -X GET "http://localhost:8000/api/images/1"
```

#### 删除图片

```bash
curl -X DELETE "http://localhost:8000/api/images/1"
```

## 剪贴板监控工具

监控剪贴板中的图片并自动上传到服务器。

### 使用方法

```bash
python clipboard_monitor.py
```

在脚本中修改服务器地址：

```python
API_URL = 'http://your-server:8000/api/images/upload'
```

## 项目结构

```
.
├── backend/
│   ├── app/
│   │   ├── api/           # API路由
│   │   ├── core/          # 业务逻辑
│   │   ├── db/            # 数据库配置
│   │   └── models/        # 数据模型
│   ├── run.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/         # 页面组件
│   │   ├── components/    # UI组件
│   │   ├── services/      # API服务
│   │   └── types/         # 类型定义
│   └── package.json
├── clipboard_monitor.py   # 剪贴板监控工具
└── README.md
```

## 部署

### 后端

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 前端

```bash
cd frontend
pnpm build
```