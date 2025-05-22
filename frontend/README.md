# 图床服务 | Image Hosting Service

一个简单易用的图片上传和管理服务，部署本地后，复制图片地址可直接访问。

![首页.png](%E9%A6%96%E9%A1%B5.png)
A simple and easy-to-use image upload and management service for NC Testing Center.

## 功能特点 | Features

- 🖼️ 图片上传：支持拖拽上传或点击选择图片文件node
- 📝 图片描述：为每张上传的图片添加可选描述
- 🔍 模糊搜索：根据文件名或描述快速查找已上传图片
- 📋 链接复制：一键复制图片URL，方便在其他地方使用
- 🗑️ 图片管理：查看和删除已上传的图片

---

- 🖼️ Image Upload: Support for drag-and-drop or click-to-select image files
- 📝 Image Description: Add optional descriptions to each uploaded image
- 🔍 Fuzzy Search: Quickly find uploaded images by filename or description
- 📋 URL Copying: One-click copy image URLs for use elsewhere
- 🗑️ Image Management: View and delete uploaded images

## 技术栈 | Tech Stack

- **前端 | Frontend**: React, TypeScript, Ant Design
- **样式 | Styling**: Tailwind CSS
- **请求处理 | API Requests**: Axios
- **构建工具 | Build Tool**: Vite

## 安装和运行 | Installation & Setup

### 前提条件 | Prerequisites

- Node.js (v14.0或更高版本)
- npm 或 yarn

### 安装步骤 | Installation Steps

1. 克隆代码库 | Clone the repository
   ```bash
   git clone https://github.com/hankerbiao/picture-beg.git
   cd image-hosting-service/frontend
   ```

2. 安装依赖 | Install dependencies
   ```bash
   pnpm install
   ```

3. 启动开发服务器 | Start the development server
   ```bash
   pnpm run dev
   ```

4. 构建生产版本 | Build for production
   ```bash
   pnpm run build
   ```

## 使用指南 | Usage Guide

### 上传图片 | Uploading Images

1. 点击或拖拽图片到上传区域
2. 可选填写图片描述
3. 点击"开始上传"按钮

### 管理图片 | Managing Images

- 使用搜索框按文件名或描述查找图片
- 点击图片缩略图可预览大图
- 使用复制按钮获取图片URL
- 使用删除按钮移除不需要的图片

## 项目结构 | Project Structure

```
frontend/
├── public/             # 静态资源
├── src/
│   ├── components/     # React组件
│   ├── pages/          # 页面组件
│   ├── services/       # API服务
│   ├── types/          # TypeScript类型定义
│   ├── App.tsx         # 应用主组件
│   └── main.tsx        # 应用入口
├── package.json        # 项目依赖
└── tsconfig.json       # TypeScript配置
```

## 许可证 | License

[MIT](LICENSE)

## 贡献 | Contributing

欢迎提交问题和功能请求。Pull requests也受欢迎。

Issues and feature requests are welcome. Pull requests are also welcome. 