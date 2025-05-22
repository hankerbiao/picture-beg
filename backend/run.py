import uvicorn
import os
from dotenv import load_dotenv

if __name__ == "__main__":
    # 加载环境变量
    load_dotenv()
    
    # 启动服务
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 