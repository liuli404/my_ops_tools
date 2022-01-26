from datetime import datetime
import webhook
import time


def time_transform(gmt_time):
    time_format = '%b %d %H:%M:%S %Y GMT'
    format_time = datetime.strptime(gmt_time, time_format)
    return format_time


def read_log(log_name):
    try:
        with open(log_name, "r") as logfile:
            for line in logfile:
                node = line.split(',')
                domain_name = node[0]
                start_time = node[1].split('=')[1]
                f_start_time = time_transform(start_time)
                expire_time = node[2].split('=')[1].replace('\n', '').replace('\r', '')
                f_expire_time = time_transform(expire_time)
                # 获取当前时间
                local_time = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                # 计算剩余时间
                available_time = str(f_expire_time - local_time).split()[0]
                if int(available_time) <= 30:
                    print(f'域名：{domain_name}\nSSL证书到期日期：{f_expire_time}\n剩余时间：{available_time} 天')
                    # webhook.send_msg(domain_name, f_expire_time, available_time)
    except Exception as e:
        webhook.send_err(str(e))

if __name__ == '__main__':
    read_log('/opt/shell/ssl_check/log.out')
