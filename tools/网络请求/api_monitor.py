import requests
import json
import time


def send_http_err(name, http_code):
    """
    发送指定消息
    :param name:
    :param http_code:
    :return:
    """
    # 微信 webhook 链接
    wx_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=4794df11-557e-4690-a8ea-9bfaf4aca474"
    message = f"<font color=\"warning\"> {name} </font>登录接口异常。\n> 接口状态码:<font color=\"comment\"> {http_code}  </font>"
    data = json.dumps({"msgtype": "markdown", "markdown": {"content": message}})
    requests.post(wx_url, data, auth=('Content-Type', 'application/json'))


def send_time_out(name, response_time):
    """
    发送指定消息
    :param name:
    :param response_time:
    :return:
    """
    # 微信 webhook 链接
    wx_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=4794df11-557e-4690-a8ea-9bfaf4aca474"
    message = f"<font color=\"warning\"> {name} </font>登录接口异常。\n> 响应时间超时:<font color=\"comment\"> {response_time} s  </font>"
    data = json.dumps({"msgtype": "markdown", "markdown": {"content": message}})
    requests.post(wx_url, data, auth=('Content-Type', 'application/json'))


def get_token(url):
    http_code = requests.get(url).status_code
    response_time = requests.get(url).elapsed.total_seconds()
    return http_code, response_time


if __name__ == '__main__':
    url_dict = {
        'chest_mini': 'https://xt.pptooo.com',
        'chest_pc': 'https://chestsaas.pptooo.com/?living=1&plant=1',
        'spa': 'https://apis.asdoctor.net/internetHospitalWs/getToken/getToken?livingId=&account=admin&password=yhnmkl&type=',
        'chest': 'https://chestapi.pptooo.com/saasWs/getToken/getToken?account=admin&password=yhmkl&livingId=1',
        'phak': 'https://phakapi.pptooo.com/internetHospitalWs/getToken/getToken?account=admin&password=yhn@mkl9527&livingId=1'
    }
    for url in url_dict:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 获取状态码、响应时间
        http_code, response_time = get_token(url_dict[url])

        # 判断状态码
        if http_code == 200:
            print(f"{timestamp}--{url} 项目服务正常，状态码为：{http_code}")
        else:
            send_http_err(f"生产环境--{url}", http_code)
        # 判断响应时间
        if response_time < 3:
            print(f"{timestamp}--{url} 项目服务正常，响应时间：{response_time}s")
        else:
            send_time_out(f"生产环境--{url}", response_time)
