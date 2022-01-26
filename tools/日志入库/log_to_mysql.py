import time
from datetime import datetime
from datetime import timedelta
import pymysql

# mysql 配置
MYSQL_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'passwd': 'Bj172jwpHG36eAKk',
    'db': 'tuniu_nginx_log',
    'charset': "utf8"
}


# 建表函数
def create_table(table_name):
    db = pymysql.connect(**MYSQL_CONFIG)  # 数据库连接
    cur = db.cursor()  # 游标对象
    drop_sql = f"DROP TABLE IF EXISTS `{table_name}`;"
    create_sql = f"CREATE TABLE `{table_name}` (" \
                 f"`id` int ( 11 ) NOT NULL AUTO_INCREMENT," \
                 f"`IP` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL," \
                 f"`Time` date NULL DEFAULT NULL," \
                 f"`Methods` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL," \
                 f"`Source` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL," \
                 f"`Protocol` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL," \
                 f"`Status` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL," \
                 f"`Http_referer` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL," \
                 f"`UA` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL," \
                 f"`Host` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL," \
                 f"PRIMARY KEY (`id`) USING BTREE);"
    try:
        cur.execute(drop_sql)
        cur.execute(create_sql)
        print('数据表创建成功！')
        cur.close()
        db.close()
    except pymysql.Error as e:
        print("数据表创建失败：%s" % e)
        db.close()


# 插入函数
def insert_data(table_name, value):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    db = pymysql.connect(**MYSQL_CONFIG)  # 数据库连接
    cur = db.cursor()  # 游标对象
    sql = f"insert into `{table_name}` (IP, Time, Methods, Source, Protocol, Status, Http_referer, UA, Host) values('{value[0]}', '{value[1]}', '{value[2]}', '{value[3]}', '{value[4]}', '{value[5]}', '{value[6]}', '{value[7]}', '{value[8]}')"
    try:
        cur.execute(sql)
        print(f'{timestamp} -- {value[0]} 数据插入成功！')
        db.commit()
        cur.close()
        db.close()
    except pymysql.Error as e:
        print(f'{timestamp} -- {value[0]} 数据插入失败：{e}')
        db.rollback()
        db.close()


# 分析日志
def analyze_log(log_name, table_name):
    with open(log_name, "r") as logfile:
        for line in logfile:
            nodes = line.split()
            _nodes = line.split('"')
            ip = nodes[0]
            nginx_time = nodes[3][1:-1].replace(":", " ", 1)  # 将时间转换为 17/Jun/2017 12:43:4格式
            date_time = str(datetime.strptime(nginx_time, "%d/%b/%Y %H:%M:%S"))  # 将时间格式化为 2017-06-17 12:43:04
            methods = nodes[5][1:]
            source = nodes[6]
            protocol = nodes[7][:-1]
            status = nodes[8]
            http_referer = nodes[10]
            ua = _nodes[5]
            http_x_forwarded_for = _nodes[6]
            request_time = _nodes[10]
            host = _nodes[11]
            res = [ip, date_time, methods, source, protocol, status, http_referer, ua, host]
            insert_data(table_name, res)


if __name__ == '__main__':
    yesterday = datetime.today().date() - timedelta(days=1)
    table_name = 'access_' + str(yesterday)
    log_name = '/opt/nginx1.4/logs/access_tuniu_web.log_' + str(yesterday)
    create_table(table_name)
    analyze_log(log_name, table_name)
