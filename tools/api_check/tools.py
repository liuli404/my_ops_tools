import requests


def get_status_code(url):
    """
    根据输入的url，获取对应的http状态码
    :param url: 需要测试的url
    :return: 状态码
    """
    res = requests.get(url)
    return res.status_code
