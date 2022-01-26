#!/usr/bin/env bash
# Author: liuli <liuli@jiankang.com>
# Version: v1.0, 2022/01/25
# Sys: CentOS 7.9.2009
# Features: 实现 MySQL 数据库的 SQL 备份
# Prepare：mysqldump 工具已安装

set -x

app_home="/opt/shell/mysql_to_oss"
bin_dir="${app_home}/bin"
config_dir="${app_home}/config"
data_dir="${app_home}/data"
logs_dir="${app_home}/logs"

oss_bucket="baikang-bak"
oss_exe="${bin_dir}/ossutil64"
oss_config="${config_dir}/ossutilconfig"
oss_endpoint="https://oss-cn-zhangjiakou-internal.aliyuncs.com"
oss_accessKeyID="LTAI4GDxFkxCHKEBDPtratno"
oss_accessKeySecret="1qXDjs06cIaCMVcCsf3R9petp1B6pw"

mysql_host="127.0.0.1"
mysql_port="23306"
mysql_user="root"
mysql_passwd="J!ZazKTCeH5@"
mysql_db="temp-tenant"
mysql_dump="/usr/bin/mysqldump"

now_time=$(date '+%Y%m%d-%H%M')
sql_file=${data_dir}/${mysql_db}_${now_time}.sql
cloud_dir="oss://${oss_bucket}/172.16.0.215/mysql/"

dir_check() {
  if [ ! -d "$1" ]; then
    mkdir -p "$1"
  fi
}

dir_check ${app_home}
dir_check ${bin_dir}
dir_check ${data_dir}
dir_check ${config_dir}
dir_check ${logs_dir}

if [ ! -f "${oss_exe}" ]; then
  wget http://gosspublic.alicdn.com/ossutil/1.7.8/ossutil64 -O ${oss_exe}
  chmod 755 ${oss_exe}
fi

if [ ! -f "${oss_config}" ]; then
  echo "[Credentials]" >> ${oss_config}
  echo "language=CH" >> ${oss_config}
  echo "endpoint=${oss_endpoint}" >> ${oss_config}
  echo "accessKeyID=${oss_accessKeyID}" >> ${oss_config}
  echo "accessKeySecret=${oss_accessKeySecret}" >> ${oss_config}
fi

rm -rf ${data_dir}/*.zip
${mysql_dump} -h${mysql_host} -u${mysql_user} -P${mysql_port} -p${mysql_passwd} --databases ${mysql_db} > "${sql_file}"
zip -qrjm ${data_dir}/"${now_time}".zip "${sql_file}"
nohup ${oss_exe} cp -r ${data_dir}/"${now_time}".zip ${cloud_dir} &>> ${logs_dir}/upload.log

