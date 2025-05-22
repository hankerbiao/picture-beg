from sqlmodel import Session, SQLModel, create_engine
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()


password = 'Mysql@123'
encoded_password = quote_plus(password)
DATABASE_URL=f"mysql+pymysql://mysql:{encoded_password}@10.17.48.246:3306/nettrix_dev"

# 创建数据库引擎
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    """创建数据库表"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """获取数据库会话"""
    with Session(engine) as session:
        yield session 