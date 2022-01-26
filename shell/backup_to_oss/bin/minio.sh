#!/usr/bin/env bash
# Author: liuli <liuli@jiankang.com>
# Version: v1.0, 2022/01/24
# Sys: CentOS 7.9.2009
# Features: 将 minio 文件数据备份至 oss
# Prepare：oss 创建 bucket

set -x

app_home="/opt/shell/minio_to_oss"
bin_dir="${app_home}/bin"
config_dir="${app_home}/config"
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

local_dir1="/mnt/minio/data/mybucket/datas/image/${last_year}/${last_mon}/${last_day}"
local_dir2="/mnt/minio/data/mybucket/datas/pdf/${last_year}/${last_mon}/${last_day}"
local_dir3="/mnt/minio/data/mybucket/datas/video/${last_year}/${last_mon}/${last_day}"

cloud_dir1="oss://${oss_bucket}/172.16.0.212/minio/datas/image/${last_year}/${last_mon}/${last_day}"
cloud_dir2="oss://${oss_bucket}/172.16.0.212/minio/datas/pdf/${last_year}/${last_mon}/${last_day}"
cloud_dir3="oss://${oss_bucket}/172.16.0.212/minio/datas/video/${last_year}/${last_mon}/${last_day}"

dir_check() {
  if [ ! -d "$1" ]; then
    mkdir -p "$1"
  fi
}

dir_check ${app_home}
dir_check ${bin_dir}
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

nohup ${oss_exe} cp -r ${local_dir1} ${cloud_dir1} &>> ${logs_dir}/upload_img.log
nohup ${oss_exe} cp -r ${local_dir2} ${cloud_dir2} &>> ${logs_dir}/upload_pdf.log
nohup ${oss_exe} cp -r ${local_dir3} ${cloud_dir3} &>> ${logs_dir}/upload_vde.log

