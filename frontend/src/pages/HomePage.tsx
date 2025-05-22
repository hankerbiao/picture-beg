import React, { useState, useEffect } from 'react';
import { Typography, Layout, Card, Spin, Badge, Input } from 'antd';
import { CloudUploadOutlined, PictureOutlined, SearchOutlined } from '@ant-design/icons';
import UploadImage from '../components/UploadImage';
import ImageList from '../components/ImageList';
import { getImages } from '../services/api';
import { ImageType } from '../types/image';

const { Title } = Typography;
const { Content, Footer } = Layout;
const { Search } = Input;

const HomePage: React.FC = () => {
  const [images, setImages] = useState<ImageType[]>([]);
  const [filteredImages, setFilteredImages] = useState<ImageType[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [refreshKey, setRefreshKey] = useState<number>(0);
  const [searchTerm, setSearchTerm] = useState<string>('');

  // 加载图片列表
  useEffect(() => {
    const fetchImages = async () => {
      setLoading(true);
      try {
        const data = await getImages();
        setImages(data);
        setFilteredImages(data);
      } catch (error) {
        console.error('Failed to fetch images:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchImages();
  }, [refreshKey]);

  // 上传成功后刷新列表
  const handleUploadSuccess = () => {
    setRefreshKey(prev => prev + 1);
  };

  // 搜索图片
  const handleSearch = (value: string) => {
    setSearchTerm(value);
    if (!value.trim()) {
      setFilteredImages(images);
      return;
    }

    const filtered = images.filter(image => {
      const lowerValue = value.toLowerCase();
      return (
        image.original_filename.toLowerCase().includes(lowerValue) ||
        (image.description?.toLowerCase().includes(lowerValue) || false)
      );
    });
    
    setFilteredImages(filtered);
  };

  return (
    <Layout>
      <Content className="py-8 px-4">
        <div className="page-container">
          <Title level={2} className="page-title">NC测试中心图床服务</Title>
          
          <Card
            className="upload-container shadow-sm"
            bordered={false}
            title={
              <div className="flex items-center">
                <CloudUploadOutlined className="mr-2 text-xl" style={{ color: '#1890ff' }} />
                <span>上传图片</span>
              </div>
            }
          >
            <UploadImage onSuccess={handleUploadSuccess} />
          </Card>
          
          <Card
            className="images-container shadow-sm"
            bordered={false}
            title={
              <div className="flex items-center">
                <PictureOutlined className="mr-2 text-xl" style={{ color: '#1890ff' }} />
                <span>已上传图片</span>
                {filteredImages.length > 0 && (
                  <Badge 
                    count={filteredImages.length} 
                    style={{ backgroundColor: '#1890ff', marginLeft: '8px' }}
                  />
                )}
              </div>
            }
            extra={
              <div className="flex items-center">
                {loading && <Spin size="small" className="mr-3" />}
                <Search
                  placeholder="搜索文件名或描述"
                  allowClear
                  enterButton={<SearchOutlined />}
                  onSearch={handleSearch}
                  onChange={(e) => handleSearch(e.target.value)}
                  style={{ width: 250 }}
                  size="middle"
                />
              </div>
            }
          >
            <ImageList 
              images={filteredImages} 
              loading={loading} 
              onDelete={handleUploadSuccess} 
            />
          </Card>
        </div>
      </Content>
      
      <Footer className="app-footer">
        NC测试中心图床服务 ©{new Date().getFullYear()} Created with React & Ant Design
      </Footer>
    </Layout>
  );
};

export default HomePage; 