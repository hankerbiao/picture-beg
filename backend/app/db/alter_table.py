import pymysql
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库连接参数
password = 'Mysql@123'
encoded_password = quote_plus(password)
host = '10.17.48.246'
port = 3306
user = 'mysql'
database = 'nettrix_dev'

def alter_table():
    """修改pdfconversion表的列类型"""
    connection = None
    try:
        # 连接到数据库
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        
        # 创建游标对象
        cursor = connection.cursor()
        
        # 修改text_content列为LONGTEXT类型
        cursor.execute("ALTER TABLE pdfconversion MODIFY COLUMN text_content LONGTEXT;")
        print("成功修改text_content列为LONGTEXT类型")
        
        # 修改processed_text列为LONGTEXT类型
        cursor.execute("ALTER TABLE pdfconversion MODIFY COLUMN processed_text LONGTEXT;")
        print("成功修改processed_text列为LONGTEXT类型")
        
        # 提交更改
        connection.commit()
        print("表结构修改成功")
        
    except Exception as e:
        print(f"修改表结构时出错: {e}")
    finally:
        # 关闭连接
        if connection:
            connection.close()

if __name__ == "__main__":
    alter_table() 