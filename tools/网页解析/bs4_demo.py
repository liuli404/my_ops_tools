import os
from bs4 import BeautifulSoup
import openpyxl
from openpyxl import workbook
from openpyxl import load_workbook


# 取出问卷用户列表的姓名、身份证、电话、创建时间
def parse_user_html(doc):
    """
    解析 html 文档，获取患者的id、姓名、身份证、电话、创建时间
    :param doc: html 文档
    :return: user_info = [patient_id, name, create_time, phone, id_card]
    """
    # 将 html 文档中 tbody 块的内容赋值给 soup 变量
    soup = BeautifulSoup(doc, 'html.parser').body.tbody.contents
    # 对 '\n' 处理：去重
    user_list = list(set(soup))
    # 对 '\n' 处理：移除 '\n' 元素
    user_list.remove('\n')
    user_info_list = []
    for tr in user_list:
        # 将每个 tr 封装成 bs 对象
        tr_soup = BeautifulSoup(f'<html>{tr}</html>', 'html.parser')
        # 患者姓名
        name = tr_soup.find(target="_blank").text.strip()
        # 创建时间
        create_time = tr_soup.find(name='td', attrs={'class': 'am-show-lg-only am-text-nowrap'}).text.strip()
        # 电话
        phone = tr_soup.find(name='td', attrs={'class': 'am-show-md-up am-text-nowrap'}).find_next_sibling().find_next_sibling().text.strip()
        # 身份证
        id_card = tr_soup.find(name='td', attrs={'class': 'am-show-md-up am-text-nowrap'}).find_next_sibling().text.strip()
        # patient_id
        patient_id = tr_soup.find('a').attrs['href'].split('/')[-1].split('.')[0]
        # 患者基本信息
        user_info = [patient_id, name, create_time, phone, id_card]
        user_info_list.append(user_info)
    return user_info_list


# 取出用户的问卷列表：patient_id、创建时间、类型、状态、问卷id
def parse_question_html(doc):
    soup = BeautifulSoup(doc, 'html.parser').body.tbody.contents
    # 对 '\n' 处理：去重
    question_list = list(set(soup))
    # 对 '\n' 处理：移除 '\n' 元素
    question_list.remove('\n')
    question_info_list = []
    for tr in question_list:
        # 将每个 tr 封装成 bs 对象
        tr_soup = BeautifulSoup(f'<html>{tr}</html>', 'html.parser')
        # 问卷创建时间
        question_create_time = tr_soup.find(name='td', attrs={'class': "am-text-nowrap"}).text
        # 类型
        question_type = tr_soup.find(name='td', attrs={'class': "am-text-nowrap"}).find_next_sibling().text
        # 状态
        question_status = tr_soup.find(name='td', attrs={'class': "am-text-nowrap"}).find_next_sibling().find_next_sibling().text
        # 问卷id
        question_id = tr_soup.find('a').attrs['href'].split('/')[-3]
        # patient_id
        patient_id = tr_soup.find('a').attrs['href'].split('/')[-1].split('.')[0]
        question_info = [patient_id, question_create_time, question_type, question_status, question_id]
        question_info_list.append(question_info)
    return question_info_list


# 创建表格
def create_excel(excel_name, excel_data):
    wb = openpyxl.Workbook()
    ws = wb.active
    # 写入表头
    ws.append([
        '主订单编号',
        '选购商品',
        '商品规格',
        '商品数量',
        '买家留言',
        '订单状态',
        '收件人',
        '收件人手机号',
        '收件地址'
    ])
    # 写入数据
    for i in range(len(excel_data)):
        ws.append(excel_data[i])
    # 保存表格
    if os.path.exists(excel_name):
        os.remove(excel_name)
        wb.save(excel_name)
    else:
        wb.save(excel_name)


# 解析商品div块
def parse_items_div(doc):
    # 取出商品div块
    soup = BeautifulSoup(doc, 'html.parser').find_all(name='div', attrs={"class": "index_tableRow__tpbkM mortise-rich-table-row"})
    # 取出每个商品div块内的有用信息
    items_list = []
    for i in range(len(soup)):
        # 订单号
        order_id = BeautifulSoup(f'<html>{soup[i]}</html>', 'html.parser').find_all(name='div', attrs={'class': "index_content__3R2D9"})[0].text.split('：')[-1]
        # 选购商品
        item_name = BeautifulSoup(f'<html>{soup[i]}</html>', 'html.parser').find_all(name='div', attrs={'class': "index_ellipsis__29MP5 undefined"})[0].text
        item_type = BeautifulSoup(f'<html>{soup[i]}</html>', 'html.parser').find_all(name='div', attrs={'class': "index_ellipsis__29MP5 undefined"})[1].text
        # 商品数量
        item_num = BeautifulSoup(f'<html>{soup[i]}</html>', 'html.parser').find_all(name='div', attrs={'class': "table_comboNum__1pAh5"})[0].text.split('x')[-1]
        # 订单状态
        order_status = BeautifulSoup(f'<html>{soup[i]}</html>', 'html.parser').find_all(name='div', attrs={'class': "index_cell__35tuI"})[5].text[0:3]
        # 收件人姓名、手机号、地址
        consumer_name = BeautifulSoup(f'<html>{soup[i]}</html>', 'html.parser').find_all(name='div', attrs={'class': "index_locationDetail__2IqFq"})[0].text.split('，')[0]
        consumer_phone = BeautifulSoup(f'<html>{soup[i]}</html>', 'html.parser').find_all(name='div', attrs={'class': "index_locationDetail__2IqFq"})[0].text.split('，')[1]
        consumer_address = BeautifulSoup(f'<html>{soup[i]}</html>', 'html.parser').find_all(name='div', attrs={'class': "index_locationDetail__2IqFq"})[0].text.split('，')[2]
        # 备注
        remarks = BeautifulSoup(f'<html>{soup[i]}</html>', 'html.parser').find_all(name='div', attrs={'class': "index_ellipsis__29MP5 undefined"})
        if len(remarks) == 6:
            remark = remarks[4].text + remarks[5].text
            item_info = [order_id, item_name, item_type, item_num, remark, order_status, consumer_name, consumer_phone, consumer_address]
            items_list.append(item_info)
        elif len(remarks) == 5:
            remark = remarks[4].text
            item_info = [order_id, item_name, item_type, item_num, remark, order_status, consumer_name, consumer_phone, consumer_address]
            items_list.append(item_info)
        elif len(remarks) == 4 or len(remarks) == 3:
            remark = ''
            item_info = [order_id, item_name, item_type, item_num, remark, order_status, consumer_name, consumer_phone, consumer_address]
            items_list.append(item_info)

        else:
            print(f'{remarks}：备注信息获取异常！！！')
    return items_list


if __name__ == '__main__':
    # 解析网页
    html_doc = open('订单管理.html', encoding='UTF-8').read()
    item_info_list = parse_items_div(html_doc)
    # 创建表格
    create_excel('test.xlsx', item_info_list)
