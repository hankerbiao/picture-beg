import axios from 'axios';
import { ImageType } from '../types/image';

// 创建axios实例
const api = axios.create({
  baseURL: '',
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