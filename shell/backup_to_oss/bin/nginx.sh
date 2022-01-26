#!/usr/bin/env bash
# Author: liuli <liuli@jiankang.com>
# Version: v1.0, 2022/01/25
# Sys: CentOS 7.9.2009
# Features: 将 nginx 相关文件备份至 oss
# Prepare：oss 创建 bucket

set -x

app_home="/opt/shell/nginx_to_oss"
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

last_year=$(( $(date -d yesterday +%Y) + 0 ))
last_mon=$(( $(date -d yesterday +%m) + 0 ))
last_day=$(( $(date -d yesterday +%d) + 0 ))

html_file="/usr/share/nginx/html"
conf_file="/etc/nginx/"
logs_file="/var/log/nginx/"

cloud_dir="oss://${oss_bucket}/172.16.0.212/nginx/"


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

rm -rf ${data_dir}/*.tar.gz
tar -zcPf ${data_dir}/nginx_${last_year}_${last_mon}_${last_day}.tar.gz ${conf_file} ${html_file} ${logs_file}
nohup ${oss_exe} cp -r ${data_dir}/nginx_${last_year}_${last_mon}_${last_day}.tar.gz ${cloud_dir} &>> ${logs_dir}/upload.log

