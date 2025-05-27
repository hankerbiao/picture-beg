import axios from 'axios';
import { ImageType } from '../types/image';

// 创建axios实例
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// 获取所有图片
export const getImages = async (): Promise<ImageType[]> => {
  const response = await api.get('/api/images');
  return response.data;
};

// 上传图片
export const uploadImage = async (formData: FormData): Promise<ImageType> => {
  const response = await api.post('/api/images/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

// 删除图片
export const deleteImage = async (id: number): Promise<void> => {
  await api.delete(`/api/images/${id}`);
};

// PDF Conversion API endpoints - 修正为正确的API路径
const API_BASE_URL = 'http://127.0.0.1:8000';
const PDF_API_PATH = '/api/pdfs'; // 修正为正确的PDF API路径

// 使用axios实例进行PDF转换
export const convertPDF = async (formData: FormData) => {
  try {
    // 检查FormData是否包含file
    let hasFile = false;
    formData.forEach((value, key) => {
      if (key === 'file') {
        hasFile = true;
        console.log('FormData contains file:', value);
      } else if (key === 'description') {
        console.log(`FormData ${key}:`, value);
      }
    });

    if (!hasFile) {
      throw new Error('表单中缺少文件');
    }

    // 使用正确的PDF转换API路径
    const response = await api.post(`${PDF_API_PATH}/convert`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        const percentCompleted = Math.round((progressEvent.loaded * 100) / (progressEvent.total || 100));
        console.log(`上传进度: ${percentCompleted}%`);
      }
    });
    
    return response.data;
  } catch (error: any) {
    console.error('PDF转换请求失败:', error);
    if (error.response) {
      // 服务器响应了错误状态码
      console.error('响应状态:', error.response.status);
      console.error('响应数据:', error.response.data);
      throw new Error(error.response.data.detail || '服务器返回错误');
    } else if (error.request) {
      // 请求已发送但没有收到响应
      console.error('未收到响应:', error.request);
      throw new Error('服务器未响应，请检查网络连接');
    } else {
      // 请求设置时出现问题
      throw error;
    }
  }
};

// 获取转换记录
export const getConversions = async () => {
  try {
    const response = await api.get(`${PDF_API_PATH}`);
    return response.data;
  } catch (error) {
    console.error('获取转换记录失败:', error);
    throw error;
  }
};

// 获取单个转换记录
export const getConversion = async (id: number) => {
  try {
    const response = await api.get(`${PDF_API_PATH}/${id}`);
    return response.data;
  } catch (error) {
    console.error('获取转换记录失败:', error);
    throw error;
  }
};

// 删除转换记录
export const deleteConversion = async (id: number) => {
  try {
    await api.delete(`${PDF_API_PATH}/${id}`);
    return true;
  } catch (error) {
    console.error('删除转换记录失败:', error);
    throw error;
  }
}; 