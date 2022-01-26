#!/usr/bin/env bash
# Auth: liuli
# Version: v1.0, 2021/12/07
# Sys: CentOS 7.9
# Features: 检测 SSL 证书的到期时间


log_home=/opt/shell/ssl_check

rm -f ${log_home}/log.out
function get_cert_time(){
    echo | openssl s_client -servername $1 -connect $1:443 2>/dev/null | openssl x509 -noout -dates
}

for i in $(cat ${log_home}/domain.txt);
do
    echo $i >> ${log_home}/log.out
    get_cert_time $i >> ${log_home}/log.out
done

# 文档处理，三行合成一行
sed -i 'N;N;s/\n/,/g' ${log_home}/log.out
