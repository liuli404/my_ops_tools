import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 第三方 SMTP 服务
# 设置服务器
mail_host = "smtp.exmail.qq.com"
# 用户名
mail_user = "liuli@jiankang.com"
# smtp授权码
mail_pass = "EBzXAHgaBm7paohF"
# 发送者邮箱
sender = 'liuli@jiankang.com'
# 接收者邮件，可设置为你的QQ邮箱或者其他邮箱
receivers = ['1224979840@qq.com']

# 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
message = MIMEMultipart()
# 正文
message.attach(MIMEText('周检：http://wiki.pptooo.com/pages/viewpage.action?pageId=53051421', 'plain', 'utf-8'))
# 邮件主题
message['Subject'] = '服务器周检报告'
# 发送者
message['From'] = sender
# 接收者
message['To'] = receivers[0]

try:
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 25)
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())
    print("邮件发送成功")

except smtplib.SMTPException:
    print("Error: 无法发送邮件")
