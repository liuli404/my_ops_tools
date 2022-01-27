#!/usr/bin/env bash
# Author: liuli <liuli@jiankang.com>
# Version: v1.0, 2022/01/25
# Sys: CentOS 7.9.2009
# Features: 实现指定目录备份到 OSS
# Prepare：

# shellcheck disable=SC2154
#set -x

source ../config/env.conf
source ../lib/env_check.sh

dir_check ${bin_dir}
dir_check ${config_dir}
dir_check ${data_dir}
dir_check ${lib_dir}
dir_check ${logs_dir}
oss_check
software_check zip
software_check mysqldump
software_check elasticdump


#backup_type "mysql"
backup_type "minio"
backup_type "nginx"
backup_type "elasticsearch"
backup_type "supervisor"
backup_type "dir"


#../lib/ossutil64 cp -r ${data_dir}/* oss://${bucket_name}/${des_folder}/ -c ../config/ossutil.conf