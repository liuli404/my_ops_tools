import requests
import json

wx_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=4794df11-557e-4690-a8ea-9bfaf4aca474"


def send_msg(name, http_code, service):
    """
    发送指定消息
    :param name:
    :param http_code:
    :param service:
    :return:
    """
    send_message = f"<font color=\"warning\"> {name} </font>服务离线，请相关同事注意。\n> 状态码:<font color=\"comment\"> {http_code} </font>\n> 链接:<font color=\"comment\"> [{service}]({service}) </font>"
    data = json.dumps({"msgtype": "markdown", "markdown": {"content": send_message}})
    r = requests.post(wx_url, data, auth=('Content-Type', 'application/json'))
