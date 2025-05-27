import requests


def upload_files_to_dataset(file_paths):
    """
    向指定的数据集上传多个文件

    参数:
    - api_key: 你的 API 访问密钥
    - address: API 服务器地址（不带 http://）
    - dataset_id: 数据集的唯一标识符
    - file_paths: 一个包含要上传的文件路径的列表，例如 ['./test1.txt', './test2.pdf']

    返回:
    - requests.Response 对象
    """
    url = f"http://123.157.247.187:27100/api/v1/datasets/759295ee36af11f0a73cd65ac74b6c9e/documents"

    headers = {
        "Authorization": f"Bearer ragflow-BlNGFjOWZlMzQ2ODExZjA4N2I0ZDY1YW"
    }

    files = [('file', (path.split('/')[-1], open(path, 'rb'))) for path in file_paths]

    try:
        with requests.Session() as session:
            response = session.post(url, headers=headers, files=files).json()
            doc_id = response['data'][0]['id']
            # 解析文档：
            url_chunks = f"http://123.157.247.187:27100/api/v1/datasets/759295ee36af11f0a73cd65ac74b6c9e/chunks"
            data = {
                'document_ids': [doc_id],
            }
            chunks_response = session.post(url_chunks, headers=headers, json=data)
            return chunks_response
    except Exception as e:
        print(f"请求过程中发生异常：{e}")
        return None


if __name__ == '__main__':
    file_paths = ["./image_handler.py"]
    response = upload_files_to_dataset(file_paths)
    if response is not None:
        print("文件上传成功")
