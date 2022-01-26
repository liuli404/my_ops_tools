#!/usr/bin/env bash
# Author: liuli <liuli@jiankang.com>
# Version: v1.0, 2022/01/25
# Sys: CentOS 7.9.2009
# Features: 实现指定目录备份到 OSS
# Prepare：

set -x

source ../config/env.conf ../config/ossutil.conf

now_time=$(date +%Y-%m-%d-%H%M)
bucket_name=baikang-bak
oss_dir=172.29.117.154
local_dir=(
/opt/demo_yanghua
/opt/node-project
/opt/shell
/etc/nginx
/usr/share/nginx/html
/etc/supervisord.d
/home/mysql_sql
/home/docker/volumes/yunshi_volume/_data/wwwroot
)

mysqlpump -h127.0.0.1 -uroot -P3306 -p'c%R9emEtq3ReXqYq' --databases yyh > /home/mysql_sql/yyh.sql
mysqlpump -h127.0.0.1 -uroot -P3307 -p'c%R9emEtq3ReXqYq' --databases siyu > /home/mysql_sql/siyu.sql
mysqlpump -h127.0.0.1 -uroot -P3307 -p'c%R9emEtq3ReXqYq' --databases health > /home/mysql_sql/health.sql

for i in ${local_dir[@]}
do
        file_name=$(basename $i)
        tar -zcPf /tmp/${file_name}.tar.gz ${i}
        /home/ossutil64 cp /tmp/${file_name}.tar.gz oss://${bucket_name}/${oss_dir}/${file_name}/${file_name}_${now_time}.tar.gz
done

