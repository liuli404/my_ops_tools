
import time
import tools
import webhook

# 定义需要监控的服务关系字典
service_dict = {
    "phak-vue-saas": "https://phaksaas.pptooo.com/",
    "phak-vue-doctor": "https://phakdoctor.pptooo.com/",
    "phak-saas-ws": "https://phakapi.pptooo.com/saasWs/doc.html",
    "phak-doctor-ws": "https://phakapi.pptooo.com/doctorWs/doc.html",
    "phak-common-ws": "https://phakapi.pptooo.com/commonWs/doc.html",
    "phak-base-ms": "https://phakapi.pptooo.com/base/doc.html",
    "phak-bussiness-ms": "https://phakapi.pptooo.com/bussiness/doc.html",
    "phak-vasc-ms": "https://phakapi.pptooo.com/vasc/doc.html",
    "chest-vue-saas": "https://chestdoctor.pptooo.com/",
    "chest-vue-doctor": "https://chestdoctor.pptooo.com/",
    "chest-saas-ws": "https://chestapi.pptooo.com/saasWs/doc.html",
    "chest-common-ws": "https://chestapi.pptooo.com/commonWs/doc.html",
    "chest-base-ms": "https://chestapi.pptooo.com/base/doc.html",
    "chest-bussiness-ms": "https://chestapi.pptooo.com/bussiness/doc.html",
    "chest-vasc-ms": "https://chestapi.pptooo.com/vasc/doc.html",
    "spa-vue-saas": "https://spa.asdoctor.net/",
    "spa-vue-doctor": "https://doctor.asdoctor.net/",
    "spa-saas-ws": "https://apis.asdoctor.net/internetHospitalWs/doc.html",
    "spa-doctor-ws": "https://apis.asdoctor.net/spaDoctor/doc.html",
    "spa-common-ws": "https://apis.asdoctor.net/wsMsg/doc.html",
    "spa-base-ms": "https://apis.asdoctor.net/base/doc.html",
    "spa-bussiness-ms": "https://apis.asdoctor.net/bussiness/doc.html",
    "spa-vasc-ms": "https://apis.asdoctor.net/vasc/doc.html",
    "spa-taskCenter-ms": "https://apis.asdoctor.net/taskCenter/doc.html"
}

# 根据服务字典进行巡检
for name, service in service_dict.items():
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # 获取状态码
    http_code = tools.get_status_code(service)
    # print(f"{name}的状态码为：{http_code}")
    # 判断有无异常，有则报警 无则结束
    if http_code == 200:
        print(f"{timestamp}--{name}服务正常，状态码为：{http_code}")
    elif http_code == 502:
        webhook.send_msg(name, http_code, service)
    else:
        print(f"{timestamp}--{name}服务正常，状态码为：{http_code}")
