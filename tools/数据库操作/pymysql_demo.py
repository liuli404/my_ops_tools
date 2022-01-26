import pymysql


class Delete(object):
    def __init__(self, user_phone):
        self.MYSQL_CONFIG = {
            'host': '192.168.1.11',
            'port': 3306,
            'user': 'root',
            'passwd': '123456Aa.',
            'db': 'dev-temp-tenant'
        }
        self.user_phone = user_phone

    def func_list(self):
        self.delete_user_account()
        self.delete_wechat_user_info()
        self.delete_spa_patient()
        self.delete_user_living()
        self.delete_return_visit_arrange()
        self.delete_doctor_record()
        self.delete_spa_patient_symptom()
        self.delete_patient_check_medication()
        self.delete_patient_question_push()
        self.delete_user_role()
        self.delete_template_push_record()
        self.delete_appointment_register()
        self.delete_appointment_task_binding()
        self.delete_questionnaire_middle()
        self.delete_user()

    def delete_user_account(self):
        db = pymysql.connect(**self.MYSQL_CONFIG)  # 数据库连接
        cur = db.cursor()  # 游标对象
        sql = f"DELETE from t_user_account where account in('{self.user_phone}');"
        try:
            cur.execute(sql)
            db.commit()
            cur.close()
            db.close()
        except pymysql.Error as e:
            print("删除失败：" + str(e))
            db.rollback()
            cur.close()
            db.close()

    def delete_wechat_user_info(self):
        db = pymysql.connect(**self.MYSQL_CONFIG)  # 数据库连接
        cur = db.cursor()  # 游标对象
        sql = f"DELETE from t_wechat_user_info where  account in ('{self.user_phone}');"
        try:
            cur.execute(sql)
            db.commit()
            cur.close()
            db.close()
        except pymysql.Error as e:
            print("删除失败：" + str(e))
            db.rollback()
            cur.close()
            db.close()

    def delete_spa_patient(self):
        db = pymysql.connect(**self.MYSQL_CONFIG)  # 数据库连接
        cur = db.cursor()  # 游标对象
        sql = f"DELETE from t_spa_patient where user_id in (SELECT id from  t_user where mobile={self.user_phone});"
        try:
            cur.execute(sql)
            db.commit()
            cur.close()
            db.close()
        except pymysql.Error as e:
            print("删除失败：" + str(e))
            db.rollback()
            cur.close()
            db.close()

    def delete_user_living(self):
        db = pymysql.connect(**self.MYSQL_CONFIG)  # 数据库连接
        cur = db.cursor()  # 游标对象
        sql = f"DELETE from t_user_living where user_id in (SELECT id from  t_user where mobile={self.user_phone});"
        try:
            cur.execute(sql)
            db.commit()
            cur.close()
            db.close()
        except pymysql.Error as e:
            print("删除失败：" + str(e))
            db.rollback()
            cur.close()
            db.close()

    def delete_return_visit_arrange(self):
        db = pymysql.connect(**self.MYSQL_CONFIG)  # 数据库连接
        cur = db.cursor()  # 游标对象
        sql = f"DELETE from t_return_visit_arrange where user_id in (SELECT id from  t_user where mobile={self.user_phone});"
        try:
            cur.execute(sql)
            db.commit()
            cur.close()
            db.close()
        except pymysql.Error as e:
            print("删除失败：" + str(e))
            db.rollback()
            cur.close()
            db.close()

    def delete_doctor_record(self):
        db = pymysql.connect(**self.MYSQL_CONFIG)  # 数据库连接
        cur = db.cursor()  # 游标对象
        sql = f"DELETE from t_doctor_record where patient_id in (SELECT id from  t_user where mobile={self.user_phone});"
        try:
            cur.execute(sql)
            db.commit()
            cur.close()
            db.close()
        except pymysql.Error as e:
            print("删除失败：" + str(e))
            db.rollback()
            cur.close()
            db.close()

    def delete_spa_patient_symptom(self):
        db = pymysql.connect(**self.MYSQL_CONFIG)  # 数据库连接
        cur = db.cursor()  # 游标对象
        sql = f"DELETE from t_spa_patient_symptom where user_id in (SELECT id from  t_user where mobile={self.user_phone});"
        try:
            cur.execute(sql)
            db.commit()
            cur.close()
            db.close()
        except pymysql.Error as e:
            print("删除失败：" + str(e))
            db.rollback()
            cur.close()
            db.close()

    def delete_patient_check_medication(self):
        db = pymysql.connect(**self.MYSQL_CONFIG)  # 数据库连接
        cur = db.cursor()  # 游标对象
        sql = f"DELETE from t_patient_check_medication where user_id in (SELECT id from  t_user where mobile={self.user_phone});"
        try:
            cur.execute(sql)
            db.commit()
            cur.close()
            db.close()
        except pymysql.Error as e:
            print("删除失败：" + str(e))
            db.rollback()
            cur.close()
            db.close()

    def delete_patient_question_push(self):
        db = pymysql.connect(**self.MYSQL_CONFIG)  # 数据库连接
        cur = db.cursor()  # 游标对象
        sql = f"DELETE from t_patient_question_push where t_user_id in (SELECT id from  t_user where mobile={self.user_phone});"
        try:
            cur.execute(sql)
            db.commit()
            cur.close()
            db.close()
        except pymysql.Error as e:
            print("删除失败：" + str(e))
            db.rollback()
            cur.close()
            db.close()

    def delete_user_role(self):
        db = pymysql.connect(**self.MYSQL_CONFIG)  # 数据库连接
        cur = db.cursor()  # 游标对象
        sql = f"DELETE from t_user_role where user_id = (SELECT id   from  t_user where mobile={self.user_phone});"
        try:
            cur.execute(sql)
            db.commit()
            cur.close()
            db.close()
        except pymysql.Error as e:
            print("删除失败：" + str(e))
            db.rollback()
            cur.close()
            db.close()

    def delete_template_push_record(self):
        db = pymysql.connect(**self.MYSQL_CONFIG)  # 数据库连接
        cur = db.cursor()  # 游标对象
        sql = f"delete from t_spa_template_push_record WHERE user_id=(SELECT id   from  t_user where mobile={self.user_phone});"
        try:
            cur.execute(sql)
            db.commit()
            cur.close()
            db.close()
        except pymysql.Error as e:
            print("删除失败：" + str(e))
            db.rollback()
            cur.close()
            db.close()

    def delete_appointment_register(self):
        db = pymysql.connect(**self.MYSQL_CONFIG)  # 数据库连接
        cur = db.cursor()  # 游标对象
        sql = f"delete FROM appointment_register where patient_id =(SELECT id from t_user where mobile={self.user_phone});"
        try:
            cur.execute(sql)
            db.commit()
            cur.close()
            db.close()
        except pymysql.Error as e:
            print("删除失败：" + str(e))
            db.rollback()
            cur.close()
            db.close()

    def delete_appointment_task_binding(self):
        db = pymysql.connect(**self.MYSQL_CONFIG)  # 数据库连接
        cur = db.cursor()  # 游标对象
        sql = f"delete from appointment_task_binding where bind_id in (SELECT id FROM appointment_register where patient_id =(SELECT id from t_user where mobile={self.user_phone}));"
        try:
            cur.execute(sql)
            db.commit()
            cur.close()
            db.close()
        except pymysql.Error as e:
            print("删除失败：" + str(e))
            db.rollback()
            cur.close()
            db.close()

    def delete_questionnaire_middle(self):
        db = pymysql.connect(**self.MYSQL_CONFIG)  # 数据库连接
        cur = db.cursor()  # 游标对象
        sql = f"delete from questionnaire_middle where patient_id =(SELECT id from t_user where mobile={self.user_phone});"
        try:
            cur.execute(sql)
            db.commit()
            cur.close()
            db.close()
        except pymysql.Error as e:
            print("删除失败：" + str(e))
            db.rollback()
            cur.close()
            db.close()

    def delete_user(self):
        db = pymysql.connect(**self.MYSQL_CONFIG)  # 数据库连接
        cur = db.cursor()  # 游标对象
        sql = f"DELETE from t_user where mobile  in('{self.user_phone}');"
        try:
            cur.execute(sql)
            db.commit()
            cur.close()
            db.close()
        except pymysql.Error as e:
            print("删除失败：" + str(e))
            db.rollback()
            cur.close()
            db.close()


if __name__ == '__main__':
    pass
