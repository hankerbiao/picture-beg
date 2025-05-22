import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Layout, ConfigProvider } from 'antd';
import HomePage from './pages/HomePage';
import './styles/global.css';

const App: React.FC = () => {
  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: '#1890ff',
          borderRadius: 8,
        },
      }}
    >
      <Layout className="min-h-screen bg-gray-50">
        <Routes>
          <Route path="/" element={<HomePage />} />
        </Routes>
      </Layout>
    </ConfigProvider>
  );
};

export default App; 