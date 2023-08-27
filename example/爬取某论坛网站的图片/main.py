import requests
from bs4 import BeautifulSoup
import uuid
import multiprocessing


# 使用 bs4 对网页首页解析，对帖子标题进行筛选，获取带 GIF、动图字样的网站标题链接，并组成列表。
def get_title_list(url):
    title_list = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/80.0.3987.106 Safari/537.36 Edg/80.0.361.54'}
    res = requests.get(headers=headers, url=url)
    res.encoding = 'UTF-8'
    soup = BeautifulSoup(res.text, 'html.parser').body
    res = soup.find_all(name='a')
    for x in res:
        # 判断标题中的内容
        if "动图" in str(x) or "GIF" in str(x):
            # 将标题转换成 bs 类
            a = BeautifulSoup(f'<html>{x}</html>', 'html.parser')
            # 使用 find 方法的 attrs 属性取出 href 的内容
            uri = a.find('a').attrs['href']
            # href 的内容为标题的 uri
            title_list.append(uri)
    return title_list


# 循环网页链接，获取单个网页连接的html，并解析页面中的 img 标签，获取动图的下载地址 list
def get_img_list(url):
    img_list = []
    page_url = f"https://9k1024.com/pw/{url}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/80.0.3987.106 Safari/537.36 Edg/80.0.361.54'}
    res = requests.get(headers=headers, url=page_url)
    res.encoding = 'UTF-8'
    # 获取 id 为 read_tpc 的 div 块。
    soup = BeautifulSoup(res.text, 'html.parser').find(name="div", attrs={"id": "read_tpc"})
    # 使用find_all()方法查找所有的 <img> 标签
    img_tags = soup.find_all('img')
    # 遍历每个 <img> 标签，并获取其 src 属性值
    for img in img_tags:
        src = img['src']
        img_list.append(src)
    return img_list


# 根据url下载图片到指定目录
def download_img(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/80.0.3987.106 Safari/537.36 Edg/80.0.361.54'}
    response = requests.get(headers=headers, url=url, stream=True, timeout=30)
    if response.status_code == 200:
        file_path = "D:\\telegram"
        file_name = str(uuid.uuid4())
        # iter_content方法的chunk_size参数设置为8192字节，即每次从响应流中读取8192字节的数据块。在每次迭代中，将读取到的数据块写入到文件中。
        # 这种逐块处理响应内容的方式可以有效地处理大型文件或流式传输，而不会占用过多的内存。
        with open(f"{file_path}/{file_name}.gif", 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"{file_name}.gif------Download_Over")


if __name__ == '__main__':
    try:
        for pg_num in range(70, 90):
            print(f"开始下载第{pg_num}页内容。")
            home_url = f'https://9k1024.com/pw/thread1022.php?fid=174&page={pg_num}'
            # 对每个页面解析，获取符合条件的标题的 uri 列表
            title_uri_list = get_title_list(home_url)
            # 根据标题 uri 列表，解析每篇文章，获取文章中的图片连接列表
            for title in title_uri_list:
                img_list = get_img_list(title)
                # 根据图片链接列表，下载至本地路径
                try:
                    # 创建进程对象
                    pool = multiprocessing.Pool()  # 无参数时，使用所有cpu核
                    # pool = multiprocessing.Pool(5)    ·
                    pool.map(download_img, img_list)
                    # 关闭线程池
                    pool.close()
                    # # 线程等待
                    pool.join()
                except Exception as e:
                    print(f"下载异常：{str(e)}")
            print(f"第{pg_num}页的所有帖子图片下载结束")
    except Exception as e:
        print(f"发生了未知的异常: {str(e)}")
