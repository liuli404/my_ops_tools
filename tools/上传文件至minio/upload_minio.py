import minio
import os
from datetime import date, datetime

minioClient = minio.Minio('oss.pptooo.com',
                          access_key='OZjCRYIKg1jzJPT4',
                          secret_key='sxkAwakceTh2ksCn',
                          secure=True)


# 创建桶
def create_bucket(bucket_name="test", location="cn-north-1"):
    try:
        minioClient.make_bucket(bucket_name, location)
    except Exception as err:
        print(err)


# 列出所有对象
def list_object(bucket_name="test", prefix=None):
    objects = minioClient.list_objects(bucket_name, prefix=prefix, recursive=True)
    for obj in objects:
        print(obj.bucket_name, obj.object_name.encode('utf-8'), obj.last_modified, obj.etag, obj.size, obj.content_type)


# 上传文件
def upload_file(bucket_name, object_name, file_path, content_type='image/jpeg', metadata=None):
    minioClient.fput_object(bucket_name, object_name, file_path, content_type, metadata)


if __name__ == '__main__':
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day

    # 创建桶
    # create_bucket(bucket_name="test", location="cn-north-1")
    bucket_name = 'mybucket'

    f_path = f'/tmp/{year}/{month}/{day}/'
    f_list = os.listdir(f_path)
    for i in f_list:
        upload_file(bucket_name, f'datas/image/{year}/{month}/{day}/{i}', f_path + i)
