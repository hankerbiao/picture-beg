import React, { useState } from 'react';
import { Upload, Button, Form, Input, message, Progress } from 'antd';
import { UploadOutlined, InboxOutlined, FileImageOutlined } from '@ant-design/icons';
import type { UploadFile, UploadProps } from 'antd/es/upload/interface';
import { uploadImage } from '../services/api';

const { Dragger } = Upload;

interface UploadImageProps {
  onSuccess: () => void;
}

const UploadImage: React.FC<UploadImageProps> = ({ onSuccess }) => {
  const [fileList, setFileList] = useState<UploadFile[]>([]);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [form] = Form.useForm();

  // 处理上传
  const handleUpload = async () => {
    const values = await form.validateFields();
    
    // 添加文件
    if (fileList.length === 0) {
      message.error('请选择要上传的图片');
      return;
    }
    
    setUploading(true);
    setUploadProgress(0);
    
    try {
      // 批量上传所有文件
      const totalFiles = fileList.length;
      let successCount = 0;
      
      for (let i = 0; i < fileList.length; i++) {
        const file = fileList[i];
        const formData = new FormData();
        formData.append('file', file.originFileObj as Blob);
        
        // 添加描述 (对于批量上传，可以选择是否将描述应用到所有图片)
        if (values.description) {
          formData.append('description', values.description);
        }
        
        try {
          await uploadImage(formData);
          successCount++;
          // 更新进度
          setUploadProgress(Math.floor((successCount / totalFiles) * 100));
        } catch (error) {
          console.error(`文件 ${file.name} 上传失败:`, error);
        }
      }
      
      if (successCount === 0) {
        message.error('所有图片上传失败');
      } else if (successCount < totalFiles) {
        message.warning(`已成功上传 ${successCount}/${totalFiles} 张图片`);
        onSuccess();
      } else {
        message.success(`已成功上传 ${successCount} 张图片`);
        onSuccess();
      }
      
      setFileList([]);
      form.resetFields();
    } catch (error) {
      console.error('图片上传失败:', error);
      message.error('图片上传失败');
    } finally {
      setUploading(false);
      setUploadProgress(0);
    }
  };

  // 上传前验证
  const beforeUpload = (file: File) => {
    const isImage = file.type.startsWith('image/');
    if (!isImage) {
      message.error('只能上传图片文件!');
      return Upload.LIST_IGNORE;
    }
    
    const isLt5M = file.size / 1024 / 1024 < 5;
    if (!isLt5M) {
      message.error('图片大小不能超过5MB!');
      return Upload.LIST_IGNORE;
    }
    
    return false;
  };

  // 上传控件属性
  const uploadProps: UploadProps = {
    onRemove: (file) => {
      const index = fileList.indexOf(file);
      const newFileList = fileList.slice();
      newFileList.splice(index, 1);
      setFileList(newFileList);
    },
    beforeUpload,
    onChange(info) {
      setFileList([...info.fileList]);
    },
    fileList,
    multiple: true,
    listType: 'picture',
    showUploadList: true,
    customRequest: ({ onSuccess }) => {
      // 阻止自动上传, 改为手动上传模式
      if (onSuccess) {
        onSuccess('ok');
      }
    },
  };

  return (
    <div className="max-w-2xl mx-auto">
      <Form form={form} layout="vertical" className="mx-auto">
        <Form.Item
          name="description"
          label={
            <span className="flex items-center font-medium text-gray-700 text-sm">
              <FileImageOutlined className="mr-1" /> 图片描述 (将应用于所有图片)
            </span>
          }
          rules={[{ max: 100, message: '描述不能超过100个字符' }]}
        >
          <Input 
            placeholder="请输入图片描述(可选)" 
            className="rounded-lg py-1" 
            allowClear
            size="small"
          />
        </Form.Item>
        
        <Form.Item>
          <Dragger 
            {...uploadProps} 
            className="border-dashed border-2 hover:border-primary transition-colors duration-300"
            style={{ 
              padding: '15px 0',
              background: 'linear-gradient(145deg, #f8fafc, #f1f5f9)',
              borderRadius: '8px'
            }}
          >
            <div className="px-3">
              <p className="ant-upload-drag-icon">
                <InboxOutlined style={{ fontSize: 36, color: '#1890ff' }} />
              </p>
              <p className="ant-upload-text text-base font-medium mb-1">
                点击或拖拽图片到此区域上传
              </p>
              <p className="ant-upload-hint text-gray-500 text-sm">
                支持批量上传多张图片，单张图片大小不超过5MB
              </p>
              <div className="mt-2 text-xs text-gray-400">
                支持格式: JPG, PNG, GIF, WEBP...
              </div>
            </div>
          </Dragger>
        </Form.Item>
        
        {uploading && uploadProgress > 0 && (
          <Form.Item>
            <Progress percent={uploadProgress} status="active" />
          </Form.Item>
        )}
        
        <Form.Item>
          <div className="flex justify-center">
            <Button
              onClick={handleUpload}
              loading={uploading}
              icon={<UploadOutlined />}
              disabled={fileList.length === 0}
              className="px-6 h-9 font-medium shadow-sm"
            >
              {uploading ? '上传中...' : `上传 ${fileList.length} 张图片`}
            </Button>
          </div>
        </Form.Item>
      </Form>
    </div>
  );
};

export default UploadImage; 