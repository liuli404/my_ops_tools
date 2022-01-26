import requests
import json

# 公司群
# wx_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=4794df11-557e-4690-a8ea-9bfaf4aca474"
# 测试群
wx_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=2723645c-8252-4e29-9889-24462052f371"


def send_msg(domain_name, f_expire_time, available_time):
    """
    发送指定消息
    :param name:
    :param http_code:
    :param service:
    :return:
    """
    send_message = f"域名：<font color=\"info\"> {domain_name} </font> 安全证书即将到期\n>到期日期：<font color=\"comment\"> {f_expire_time} </font>\n>剩余天数：<font color=\"warning\"> {available_time} </font> 天"
    data = json.dumps({"msgtype": "markdown", "markdown": {"content": send_message}})
    r = requests.post(wx_url, data, auth=('Content-Type', 'application/json'))


def send_err(err_info):
    send_message = f"<font color=\"warning\"> 域名证书检查脚本执行失败！！！ </font>\n><font color=\"info\"> {err_info} </font>"
    data = json.dumps({"msgtype": "markdown", "markdown": {"content": send_message}})
    r = requests.post(wx_url, data, auth=('Content-Type', 'application/json'))
