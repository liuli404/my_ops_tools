import time
import pymysql
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# 加载驱动
driver = webdriver.Chrome()
# 隐式等待
driver.implicitly_wait(30)
# 显示等待
wait = WebDriverWait(driver, 30, 0.3)

# 数据库配置
MYSQL_CONFIG = {
    'host': '192.168.1.11',
    'port': 3306,
    'user': 'root',
    'passwd': '123456Aa.',
    'db': 'liuli'
}


# 统计患者问卷个数
def count_question_num(table_name):
    db = pymysql.connect(**MYSQL_CONFIG)  # 数据库连接
    cur = db.cursor()  # 游标对象
    sql = f"SELECT count(id) FROM `{table_name}`;"
    cur.execute(sql)
    data = cur.fetchone()
    cur.close()
    db.close()
    return data


# 根据id取出患者问卷信息
def get_question_list(table_name, id):
    db = pymysql.connect(**MYSQL_CONFIG)  # 数据库连接
    cur = db.cursor()  # 游标对象
    sql = f"SELECT * FROM `{table_name}` where id = {id};"
    res_list = []
    try:
        cur.execute(sql)
        results = cur.fetchall()
        for row in results:
            res_list.extend(row)
    except pymysql.Error as e:
        print("Error: " + str(e))
    cur.close()
    db.close()
    return res_list


# 打开指定网站
def open_url(url, account, passwd):
    # 将浏览器最大化显示
    driver.maximize_window()
    # 打开网页
    driver.get(url)
    # 登录
    driver.find_elements_by_class_name('el-input__inner')[0].send_keys(account)
    driver.find_elements_by_class_name('el-input__inner')[1].send_keys(passwd)
    driver.find_element_by_class_name('loginBtn').click()


# 进入患者列表页面
def into_module():
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[1]/ul/li[2]/div/span'))).click()
    time.sleep(1)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[1]/ul/li[2]/ul/li/ul/li'))).click()
    time.sleep(1)


# 根据姓名、手机号、身份证搜索患者，进入评估问卷页面
def into_user_info(condition, patient_name):
    # 输入搜索条件
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[2]/div[1]/div[2]/input'))).clear()
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[2]/div[1]/div[2]/input'))).send_keys(condition)
    time.sleep(0.5)
    # 点击搜索
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[2]/div[1]/div[6]/button[1]/span'))).click()
    time.sleep(1)
    res = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[2]/div[2]/div[3]/table/tbody/tr/td[2]/div/button/span'))).text
    try:
        if patient_name == res:
            # 点击人名
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[2]/div[2]/div[3]/table/tbody/tr/td[2]/div/button/span'))).click()
            time.sleep(0.5)
            # 点击问卷详情
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[2]/div[1]/div[3]/span[2]'))).click()
        else:
            time.sleep(3)
            # 点击搜索
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[2]/div[1]/div[6]/button[1]/span'))).click()
            # 点击人名
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[2]/div[2]/div[3]/table/tbody/tr/td[2]/div/button/span'))).click()
            time.sleep(0.5)
            # 点击问卷详情
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[2]/div[1]/div[3]/span[2]'))).click()
    except Exception as e:
        print(f'{patient_name} ----- {str(e)} 无此用户')


# 添加问卷
def add_question():
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div[2]/div[2]/div[1]/button/span').click()
    time.sleep(0.5)


# 添加整体情况问卷
def add_general(data_time, q1, q2, q3):
    # 添加问卷
    add_question()
    # 填写时间
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div[2]/div[2]/section/main/div/div[1]/div[1]/input').send_keys(data_time)
    # 点开问卷类型
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div[2]/div[2]/section/main/div/div[1]/div[2]/div/input').click()
    # 选择整体情况
    time.sleep(0.5)
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[1]/div[1]/ul/li[1]'))).click()
    time.sleep(0.5)
    # 填写整体情况问卷
    # 第一题
    time.sleep(0.1)
    wait.until(lambda x: x.find_elements_by_class_name('templateOption')[0].find_elements_by_class_name('defualtType')[q1]).click()
    # 第二题
    time.sleep(0.1)
    wait.until(lambda x: x.find_elements_by_class_name('templateOption')[1].find_elements_by_class_name('defualtType')[q2]).click()
    # 第三题
    time.sleep(0.1)
    wait.until(lambda x: x.find_elements_by_class_name('templateOption')[2].find_elements_by_class_name('defualtType')[q3]).click()
    # 点击保存
    time.sleep(0.5)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[2]/div[2]/section/main/div/div[2]/div/div[2]/button/span'))).click()
    time.sleep(0.5)


# 添加强直指数问卷
def add_basdai(data_time, q1, q2, q3, q4, q5, q6):
    # 添加问卷
    add_question()
    # 填写时间
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div[2]/div[2]/section/main/div/div[1]/div[1]/input').send_keys(data_time)
    # 点开问卷类型
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div[2]/div[2]/section/main/div/div[1]/div[2]/div/input').click()
    # 选择强直指数
    time.sleep(0.5)
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[1]/div[1]/ul/li[2]'))).click()
    time.sleep(0.5)
    # Q1
    time.sleep(0.1)
    driver.find_elements_by_class_name('templateOption')[0].find_elements_by_class_name('defualtType')[q1].click()
    # Q2
    time.sleep(0.1)
    driver.find_elements_by_class_name('templateOption')[1].find_elements_by_class_name('defualtType')[q2].click()
    # Q3
    time.sleep(0.1)
    driver.find_elements_by_class_name('templateOption')[2].find_elements_by_class_name('defualtType')[q3].click()
    # Q4
    time.sleep(0.1)
    driver.find_elements_by_class_name('templateOption')[3].find_elements_by_class_name('defualtType')[q4].click()
    # Q5
    time.sleep(0.1)
    driver.find_elements_by_class_name('templateOption')[4].find_elements_by_class_name('defualtType')[q5].click()
    # Q6
    time.sleep(0.1)
    driver.find_elements_by_class_name('templateOption')[5].find_elements_by_class_name('defualtType')[q6].click()
    # 点击保存
    time.sleep(0.5)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[2]/div[2]/section/main/div/div[2]/div/div[2]/button/span'))).click()
    time.sleep(0.5)


# 添加功能指数
def add_basfi(data_time, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10):
    # 添加问卷
    add_question()
    # 填写时间
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div[2]/div[2]/section/main/div/div[1]/div[1]/input').send_keys(data_time)
    # 点开问卷类型
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div[2]/div[2]/section/main/div/div[1]/div[2]/div/input').click()
    # 选择功能指数
    time.sleep(0.5)
    driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[1]/ul/li[3]').click()
    time.sleep(0.5)
    # Q1
    time.sleep(0.1)
    driver.find_elements_by_class_name('templateOption')[0].find_elements_by_class_name('defualtType')[q1].click()
    # Q2
    time.sleep(0.1)
    driver.find_elements_by_class_name('templateOption')[1].find_elements_by_class_name('defualtType')[q2].click()
    # Q3
    time.sleep(0.1)
    driver.find_elements_by_class_name('templateOption')[2].find_elements_by_class_name('defualtType')[q3].click()
    # Q4
    time.sleep(0.1)
    driver.find_elements_by_class_name('templateOption')[3].find_elements_by_class_name('defualtType')[q4].click()
    # Q5
    time.sleep(0.1)
    driver.find_elements_by_class_name('templateOption')[4].find_elements_by_class_name('defualtType')[q5].click()
    # Q6
    time.sleep(0.1)
    driver.find_elements_by_class_name('templateOption')[5].find_elements_by_class_name('defualtType')[q6].click()
    # Q7
    time.sleep(0.1)
    driver.find_elements_by_class_name('templateOption')[6].find_elements_by_class_name('defualtType')[q7].click()
    # Q8
    time.sleep(0.1)
    driver.find_elements_by_class_name('templateOption')[7].find_elements_by_class_name('defualtType')[q8].click()
    # Q9
    time.sleep(0.1)
    driver.find_elements_by_class_name('templateOption')[8].find_elements_by_class_name('defualtType')[q9].click()
    # Q10
    time.sleep(0.1)
    driver.find_elements_by_class_name('templateOption')[9].find_elements_by_class_name('defualtType')[q10].click()
    # 点击保存
    time.sleep(0.5)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[2]/div[2]/section/main/div/div[2]/div/div[2]/button/span'))).click()
    time.sleep(0.5)


# 添加健康指数
def add_asas(data_time, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16, q17):
    # 添加问卷
    add_question()
    # 填写时间
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div[2]/div[2]/section/main/div/div[1]/div[1]/input').send_keys(data_time)
    # 点开问卷类型
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div[2]/div[2]/section/main/div/div[1]/div[2]/div/input').click()
    # 选择健康指数
    time.sleep(0.5)
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[1]/div[1]/ul/li[4]'))).click()
    time.sleep(0.5)
    # Q1
    time.sleep(0.1)
    driver.find_elements_by_css_selector("[class='templateOption flex']")[0].find_elements_by_class_name('radioDefault')[q1].click()
    # Q2
    time.sleep(0.1)
    driver.find_elements_by_css_selector("[class='templateOption flex']")[1].find_elements_by_class_name('radioDefault')[q2].click()
    # Q3
    time.sleep(0.1)
    driver.find_elements_by_css_selector("[class='templateOption flex']")[2].find_elements_by_class_name('radioDefault')[q3].click()
    # Q4
    time.sleep(0.1)
    driver.find_elements_by_css_selector("[class='templateOption flex']")[3].find_elements_by_class_name('radioDefault')[q4].click()
    # Q5
    time.sleep(0.1)
    driver.find_elements_by_css_selector("[class='templateOption flex']")[4].find_elements_by_class_name('radioDefault')[q5].click()
    # Q6
    time.sleep(0.1)
    driver.find_elements_by_css_selector("[class='templateOption flex']")[5].find_elements_by_class_name('radioDefault')[q6].click()
    # Q7
    time.sleep(0.1)
    driver.find_elements_by_css_selector("[class='templateOption flex']")[6].find_elements_by_class_name('radioDefault')[q7].click()
    # Q8
    time.sleep(0.1)
    driver.find_elements_by_css_selector("[class='templateOption flex']")[7].find_elements_by_class_name('radioDefault')[q8].click()
    # Q9
    time.sleep(0.1)
    driver.find_elements_by_css_selector("[class='templateOption flex']")[8].find_elements_by_class_name('radioDefault')[q9].click()
    # Q10
    time.sleep(0.1)
    driver.find_elements_by_css_selector("[class='templateOption flex']")[9].find_elements_by_class_name('radioDefault')[q10].click()
    # Q11
    time.sleep(0.1)
    driver.find_elements_by_css_selector("[class='templateOption flex']")[10].find_elements_by_class_name('radioDefault')[q11].click()
    # Q12
    time.sleep(0.1)
    driver.find_elements_by_css_selector("[class='templateOption flex']")[11].find_elements_by_class_name('radioDefault')[q12].click()
    # Q13
    time.sleep(0.1)
    driver.find_elements_by_css_selector("[class='templateOption flex']")[12].find_elements_by_class_name('radioDefault')[q13].click()
    # Q14
    time.sleep(0.1)
    driver.find_elements_by_css_selector("[class='templateOption flex']")[13].find_elements_by_class_name('radioDefault')[q14].click()
    # Q15
    time.sleep(0.1)
    driver.find_elements_by_css_selector("[class='templateOption flex']")[14].find_elements_by_class_name('radioDefault')[q15].click()
    # Q16
    time.sleep(0.1)
    driver.find_elements_by_css_selector("[class='templateOption flex']")[15].find_elements_by_class_name('radioDefault')[q16].click()
    # Q17
    time.sleep(0.1)
    driver.find_elements_by_css_selector("[class='templateOption flex']")[16].find_elements_by_class_name('radioDefault')[q17].click()

    # 点击保存
    time.sleep(0.5)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[2]/div[2]/section/main/div/div[2]/div/div[2]/button/span'))).click()
    time.sleep(0.5)


# 返回患者详情页面
def into_patient_info():
    time.sleep(0.5)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[1]/span[2]/span/span'))).click()
    time.sleep(0.5)


# 关闭浏览器
def close_browser(sec):
    time.sleep(sec)
    driver.close()
    driver.quit()


if __name__ == '__main__':
    # 打开指定网站
    # open_url('https://saas.pptooo.com/', 'admin', 'yhnmkl')
    open_url('https://spa.asdoctor.net/', 'admin', 'yhnmkl')
    # 进入患者列表模块
    into_module()
    # 缩小网页
    driver.set_window_size(1000, 1025)
    # 统计问卷数量
    # count = list(count_question_num('question_doctor_filtered'))[0]
    # 查询数据
    # for i in range(count):
    for i in range(5119, 5394):
        id = i + 1
        question_list = get_question_list('question_doctor_filtered', id)

        if question_list[5] == '月填_2':
            try:
                # 根据姓名\手机号\身份证搜索患者，进入评估问卷页面
                into_user_info(question_list[4], question_list[1])
                # 整体情况问卷
                add_general(question_list[6], question_list[7], question_list[8], question_list[9])
                # BASDAI强直指数
                add_basdai(question_list[6], question_list[10], question_list[11], question_list[12], question_list[13], question_list[14], question_list[15])
                # 返回用户详情
                into_patient_info()
            except Exception as e:
                print(f'{question_list[4]}：异常-----------{e}')
        elif question_list[5] == '季填_4' or question_list[5] == '半年填_5' or question_list[5] == '一年填_7':
            # 根据姓名\手机号\身份证搜索患者，进入评估问卷页面
            try:
                into_user_info(question_list[4], question_list[1])
                # 整体情况问卷
                add_general(question_list[6], question_list[7], question_list[8], question_list[9])
                # BASDAI强直指数
                add_basdai(question_list[6], question_list[10], question_list[11], question_list[12], question_list[13], question_list[14], question_list[15])
                # BASFI功能指数
                add_basfi(question_list[6], question_list[16], question_list[17], question_list[18], question_list[19], question_list[20], question_list[21], question_list[22],
                          question_list[23], question_list[24], question_list[25])
                # ASAS-HI健康指数 0：否、1：是
                add_asas(question_list[6], question_list[26], question_list[27], question_list[28], question_list[29], question_list[30], question_list[31], question_list[32],
                         question_list[33], question_list[34], question_list[35], question_list[36], question_list[37], question_list[38], question_list[39], question_list[40],
                         question_list[41], question_list[42])
                # 返回用户详情
                into_patient_info()
            except Exception as e:
                print(f'{question_list[4]}：异常-----------{e}')
        else:
            print(f'{id}：问卷类型错误')

    # 关闭浏览器
    close_browser(3)
