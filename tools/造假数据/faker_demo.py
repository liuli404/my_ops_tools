from faker import Faker
from faker.providers import internet

"""
参考链接：
https://faker.readthedocs.io/en/master/
https://mp.weixin.qq.com/s/-64Glr5bkCtRMJMea9UmCA
"""


def create_fake_name(locale='zh_CN', num=1):
    """
    根据文化地区生成假姓名
    :param locale: 文化选项：zh_CN - Chinese (China Mainland)、zh_TW - Chinese (China Taiwan)、en_US - English (United States)
    :param num: 生成数量
    :return: 姓名列表
    """
    fake = Faker(locale=locale)
    name_list = []
    for x in range(num):
        fake_name = fake.name()
        name_list.append(fake_name)
    return name_list


def create_fake_user_info(locale='zh_CN', num=1):
    fake = Faker(locale=locale)
    user_info_list = []
    for x in range(num):
        fake_name = fake.name()
        fake_id = fake.ssn()
        fake_phone = fake.phone_number()
        fake_address = fake.address()
        user_info = [fake_name, fake_id, fake_phone, fake_address]
        user_info_list.append(user_info)
    return user_info_list


if __name__ == '__main__':
    # print(create_fake_name('zh_CN', 100))
    print(create_fake_user_info('zh_CN', 5)[0])
