#!/usr/bin/env bash
# Author: liuli <liuli@jiankang.com>
# Version: v1.0, 2022/01/25
# Sys: CentOS 7.9.2009
# Features: 函数库

# shellcheck disable=SC2154
# shellcheck disable=SC2181

source ../config/env.conf

dir_check() {
  if [ ! -d $1 ]; then
    mkdir -p $1
  fi
}

oss_check() {
  if [ ! -f "../lib/ossutil64" ]; then
  wget http://gosspublic.alicdn.com/ossutil/1.7.8/ossutil64 -O ../lib/ossutil64
  chmod 755 ../lib/ossutil64
  fi

  ../lib/ossutil64 lrb --connect-timeout 10 --read-timeout 10 -c ../config/ossutil.conf &>/dev/null
  if [ "$?" -ne 0 ]; then
    echo "OSS Connection Error !!!"
    exit $?
  fi
}

software_check() {
  case $1 in
  "zip")
    zip --version &>/dev/null
    if [ $? -ne 0 ]; then
      yum install -y zip unzip
    fi
    ;;
  "mysqldump")
  ${mysql_dump} --version &>/dev/null
    if [ $? -ne 0 ]; then
      yum install -y mysql-client
    fi
    ;;
  "elasticdump")
  ${mysql_dump} --version &>/dev/null
    if [ $? -ne 0 ]; then
      yum install -y mysql-client
    fi
    ;;
  esac
}

backup_type() {
  case $1 in
  "mysql")
    fork mysql_dump.sh
    ;;
  "minio")
    echo "minio"
    ;;
  "nginx")
    echo "nginx"
    ;;
  "elasticsearch")
    echo "elasticsearch"
    ;;
  "supervisor")
    echo "supervisor"
    ;;
  "dir")
    echo "dir"
    ;;
  *)
    echo "Please Select The Correct Type !"
    ;;
  esac
}