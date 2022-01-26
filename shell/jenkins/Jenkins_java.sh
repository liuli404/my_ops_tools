#!/usr/bin/env bash
# Author: liuli <liuli@jiankang.com>
# Version: v1.0, 2022/01/14
# Sys: CentOS 7.9.2009
# Features: java 通用发布脚本
# Prepare：① ssh 免密钥登陆配置 <ssh-copy-id user@ip> ② 客户端 supervisor 已安装
set -x

############################# 客户端服务器配置 #############################

# 客户端服务器的 IP
client_ip="192.168.1.5"

# 客户端服务器的端口
client_port="22"

# 免密登录客户端服务器的用户名
client_user="root"

############################# 项目环境配置 #############################

# supervisor 进程名
program="saas-java-ws"

# 待发布的 Jar 包名
jar_name="saas-ws-0.0.1.jar"

# 项目主目录
deploy="/opt/saas"

# 程序运行目录
app_dir="${deploy}/java"

# 配置文件目录
config_dir="${deploy}/config"

# 日志文件目录
log_dir="${deploy}/logs"

# 旧版本目录
release_dir="${deploy}/release"

############################# 环境检查区 #############################

function env_check() {
  case $1 in
  "ssh")
    ssh ${client_user}@${client_ip} -p${client_port} -o PreferredAuthentications=publickey -o StrictHostKeyChecking=no 'ls' &>/dev/null
    if [ $? -ne 0 ]; then
      echo "客户端主机免密登录异常！"
      exit $?
    fi
    ;;
  "jdk")
    ssh ${client_user}@${client_ip} -p${client_port} "java -version" &>/dev/null
    if [ $? -ne 0 ]; then
      echo "JDK 环境未安装！"
      exit $?
    fi
    ;;
  "supervisor")
    ssh ${client_user}@${client_ip} -p${client_port} "supervisord -v" &>/dev/null
    if [ $? -ne 0 ]; then
      echo "supervisor 环境未安装！"
      exit $?
    fi
    ;;
  "rsync")
    ssh ${client_user}@${client_ip} -p${client_port} "rpm -q $1" &>/dev/null
    if [ $? -ne 0 ]; then
      ssh ${client_user}@${client_ip} -p${client_port} "yum install -y $1" &>/dev/null
    fi
    ;;
  *)
    echo "环境检查异常！"
    ;;
  esac
}

function dir_check() {
  ssh ${client_user}@${client_ip} -p${client_port} "if [ ! -d $1 ]; then mkdir -p $1; fi"
}

env_check "ssh"
env_check "jdk"
env_check "supervisor"
env_check "rsync"
dir_check "${app_dir}"
dir_check "${config_dir}"
dir_check "${log_dir}"
dir_check "${release_dir}"

############################# RUNTIME #############################

app_pid=$(ssh ${client_user}@${client_ip} -p${client_port} "ps -ef | grep ${jar_name} | grep java | grep -v grep | wc -l")
if [[ ${app_pid} -eq 0 ]]; then
  find . -name ${jar_name} -type f -exec rsync --backup --backup-dir=${release_dir} --suffix="_${BUILD_ID}" {} ${client_user}@${client_ip}:${app_dir} \;
  ssh ${client_user}@${client_ip} -p${client_port} "/usr/bin/supervisorctl start ${program}"
else
  find . -name ${jar_name} -type f -exec rsync --backup --backup-dir=${release_dir} --suffix="_${BUILD_ID}" {} ${client_user}@${client_ip}:${app_dir} \;
  ssh ${client_user}@${client_ip} -p${client_port} "/usr/bin/supervisorctl restart ${program}"
fi
