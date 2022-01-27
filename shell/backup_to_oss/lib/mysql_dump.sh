#!/usr/bin/env bash
# Author: liuli <liuli@jiankang.com>
# Version: v1.0, 2022/01/25
# Sys: CentOS 7.9.2009
# Features: 实现 MySQL 数据库的 SQL 备份
# Prepare：mysqldump 工具已安装

#set -x
# shellcheck disable=SC2154
source ../config/env.conf

now_time=$(date '+%Y%m%d-%H%M')
sql_file=${data_dir}/${mysql_db}_${now_time}.sql


${mysql_dump} -h${mysql_host} -u${mysql_user} -P${mysql_port} -p${mysql_passwd} --databases ${mysql_db} > ${sql_file}
zip -qrjm ${data_dir}/${now_time}.zip ${sql_file}
nohup ${oss_exe} cp -r ${data_dir}/"${now_time}".zip ${cloud_dir} &>> ${logs_dir}/upload.log

