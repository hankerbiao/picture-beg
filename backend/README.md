# 图床服务后端

基于FastAPI的图床服务后端，为博客和其他Web应用提供图片托管和管理功能。

## 功能特点

- 图片上传（带内容类型验证）
- 通过API获取图片
- 图片元数据管理
- 静态文件服务
- RESTful API设计

## 技术栈

- **FastAPI**：现代、高速的Web框架，用于构建API
- **SQLModel**：用于数据库交互的ORM
- **Uvicorn**：用于托管应用程序的ASGI服务器
- **Python 3**：核心编程语言

## 部署指南

### 前置要求

- Python 3.9+
- 虚拟环境（推荐）

### 安装步骤

1. 克隆仓库
   ```bash
   git clone https://github.com/hankerbiao/picture-beg.git
   cd image-hosting-service/backend
   ```

2. 设置虚拟环境
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows系统: .venv\Scripts\activate
   ```

3. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

4. 创建环境变量文件
   ```bash
   cp env.example .env
   ```
   编辑`.env`文件配置你的环境设置。

### 运行应用

```bash
python run.py
```

服务器默认会在`http://localhost:8000`启动。

## API接口

### 图片API

- `POST /api/images/upload` - 上传新图片
- `GET /api/images/` - 列出所有图片
- `GET /api/images/{image_id}` - 获取特定图片详情
- `DELETE /api/images/{image_id}` - 删除图片

## 项目结构

```
backend/
├── app/
│   ├── api/              # API路由和控制器
│   ├── core/             # 核心业务逻辑
│   ├── db/               # 数据库配置
│   ├── models/           # 数据模型
│   ├── static/           # 静态文件存储
│   └── main.py           # 应用程序入口点
├── .venv/                # 虚拟环境
├── requirements.txt      # Python依赖
├── env.example           # 环境变量示例
└── run.py                # 应用程序启动器
```

## 开发指南

### 添加新功能

添加新功能时：
1. 在`app/models/`中创建适当的模型
2. 在`app/core/`中添加业务逻辑
3. 在`app/api/`中创建API端点
4. 根据需要更新文档

