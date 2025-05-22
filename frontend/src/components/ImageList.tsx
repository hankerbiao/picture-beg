import React, { useState } from 'react';
import { Table, Button, Image, Modal, message, Tooltip, Space, Card, Typography } from 'antd';
import { DeleteOutlined, CopyOutlined, ExclamationCircleOutlined } from '@ant-design/icons';
import { CopyToClipboard } from 'react-copy-to-clipboard';
import { ImageType } from '../types/image';
import { deleteImage } from '../services/api';
import './ImageList.css';

const { Text } = Typography;

interface ImageListProps {
  images: ImageType[];
  loading: boolean;
  onDelete: () => void;
}

const ImageList: React.FC<ImageListProps> = ({ images, loading, onDelete }) => {
  const [previewVisible, setPreviewVisible] = useState(false);
  const [previewImage, setPreviewImage] = useState('');
  const [previewTitle, setPreviewTitle] = useState('');
  
  // 显示图片预览
  const handlePreview = (image: ImageType) => {
    setPreviewImage(image.url);
    setPreviewTitle(image.original_filename);
    setPreviewVisible(true);
  };
  
  // 删除图片
  const handleDelete = (id: number) => {
    Modal.confirm({
      title: '确认删除',
      icon: <ExclamationCircleOutlined />,
      content: '确定要删除这张图片吗？此操作不可恢复！',
      okText: '确认',
      cancelText: '取消',
      onOk: async () => {
        try {
          await deleteImage(id);
          message.success('图片删除成功');
          onDelete();
        } catch (error) {
          console.error('Failed to delete image:', error);
          message.error('图片删除失败');
        }
      },
    });
  };
  
  // 格式化文件大小
  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
  };
  
  // 格式化日期
  const formatDate = (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const columns = [
    {
      title: '缩略图',
      dataIndex: 'url',
      key: 'thumbnail',
      width: 100,
      render: (url: string, record: ImageType) => (
        <div className="p-1">
          <Image
            src={url}
            alt={record.original_filename}
            width={70}
            height={70}
            style={{ 
              objectFit: 'cover', 
              borderRadius: '8px', 
              cursor: 'pointer',
              boxShadow: '0 2px 6px rgba(0, 0, 0, 0.1)',
              transition: 'all 0.3s ease'
            }}
            preview={false}
            onClick={() => handlePreview(record)}
            className="hover:shadow-md"
          />
        </div>
      ),
    },
    {
      title: '文件信息',
      dataIndex: 'original_filename',
      key: 'fileInfo',
      ellipsis: true,
      render: (filename: string, record: ImageType) => (
        <div className="flex flex-col">
          <Text strong ellipsis style={{ fontSize: '14px' }}>{filename}</Text>
          <Space size={8} className="text-gray-500 text-xs mt-1">
            <Text type="secondary">{formatFileSize(record.size)}</Text>
            <Text type="secondary">•</Text>
            <Text type="secondary">{record.content_type.split('/')[1]?.toUpperCase()}</Text>
          </Space>
        </div>
      ),
    },
    {
      title: '描述',
      dataIndex: 'description',
      key: 'description',
      ellipsis: true,
      render: (desc: string) => desc ? 
        <Text ellipsis style={{ maxWidth: 200 }}>{desc}</Text> : 
        <Text type="secondary" italic>无描述</Text>,
    },
    {
      title: '上传时间',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (date: string) => (
        <Text type="secondary">{formatDate(date)}</Text>
      ),
    },
    {
      title: '操作',
      key: 'actions',
      width: 180,
      render: (_: any, record: ImageType) => (
        <Space size="middle">
          <Tooltip title="预览图片">

          </Tooltip>
          <CopyToClipboard text={record.url} onCopy={() => message.success('链接已复制到剪贴板')}>
            <Tooltip title="复制链接">
              <Button 
                shape="circle" 
                icon={<CopyOutlined />}
                size="middle"
              />
            </Tooltip>
          </CopyToClipboard>
          <Tooltip title="删除图片">
            <Button 
              type="primary" 
              danger 
              shape="circle" 
              icon={<DeleteOutlined />} 
              onClick={() => handleDelete(record.id)}
              size="middle"
            />
          </Tooltip>
        </Space>
      ),
    },
  ];

  return (
    <>
      <Card 
        bordered={false} 
        className="shadow-md rounded-lg overflow-hidden"
        bodyStyle={{ padding: 0 }}
      >
        <Table
          rowKey="id"
          columns={columns}
          dataSource={images}
          loading={loading}
          pagination={{ 
            pageSize: 10,
            showTotal: (total) => `共 ${total} 条记录`,
            position: ['bottomCenter'],
            hideOnSinglePage: true
          }}
          scroll={{ x: 900 }}
          bordered={false}
          size="large"
          rowClassName="hover:bg-gray-50 transition-colors"
          className="custom-table"
        />
      </Card>
      
      <Modal
        open={previewVisible}
        title={previewTitle}
        footer={null}
        onCancel={() => setPreviewVisible(false)}
        width={800}
        centered
        className="image-preview-modal"
      >
        <img alt={previewTitle} style={{ width: '100%' }} src={previewImage} />
      </Modal>
    </>
  );
};

export default ImageList; 