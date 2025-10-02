import mysql.connector
from mysql.connector import Error
import bcrypt
import string
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from webdav3.client import Client
from Identification_face import identification_detector
import cv2
import numpy as np
import json
import os
import urllib3

def send_password(password,email,login):
    msg = MIMEMultipart()
    msg['From'] = 'ERRORZERONI@yandex.ru'
    msg['To'] = str(email)
    msg['Subject'] = 'Администратор системы посещения'
    message = 'Новый пользователь системы отправляю тебе пароль от твоего личного кабинета, где ты можешь смотреть своё посещение \n\n'+'Пароль: '+str(password)+'\nЛогин: '+str(login)
    msg.attach(MIMEText(message))
    try:
        mail_lib = smtplib.SMTP_SSL('smtp.yandex.ru',465)
        mail_lib.login("ERRORZERONI@yandex.ru","ounukprovfassyvq")
        mail_lib.sendmail('ERRORZERONI@yandex.ru',str(email),msg.as_string())
        mail_lib.quit()
        print("Письмо успешно отправлено")
    except smtplib.SMTPException:
        print("Ошибка: Невозможно отправить сообщение")

def generate_password(lenght=10):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(lenght))
    return password

def hash_password(password):
    salt = bcrypt.gensalt(rounds=8)
    hashed = bcrypt.hashpw(password.encode('utf-8'),salt)
    return hashed

class db():
    def __init__(self):
        self.config = {
            'host' : "s-3.h.filess.io",
            'database' : "Exam_socialsign",
            'password' : "7fc55fb542161bb01fa3cc3d6f5f96593ebb4962",
            'username' : "Exam_socialsign",
            'port' : "3307",
        }
        self.connection = None
        self.cursor = None
        self.detector = identification_detector()
        self.client = Client({
            'webdav_hostname': "https://webdav.cloud.mail.ru",
            'webdav_login': "Brandodio9@mail.ru",
            'webdav_password':"cw4mCk6k0fG7h5iFz0kC"
        })

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
            if self.connection.is_connected():
                print("Есть подключение")
                self.cursor = self.connection.cursor()
                return self
        except Error as e:
            print(f"Ошибка подключения: {e}")
            return None
        
    def get_stud_list(self):
        try:
            if not self.connection or not self.connection.is_connected():
                print("Нет подключения к БД")
                return []
            
            self.cursor.execute("SELECT * FROM `Student`")
            results = self.cursor.fetchall()
            return results
        except Error as e:
            print(f"Ошибка при получении данных студентов: {e}")
            return []

    def get_teacher_list(self):
        try:
            if not self.connection or not self.connection.is_connected():
                print("Нет подключения к БД")
                return []
            
            self.cursor.execute("SELECT * FROM `Teacher`")
            results = self.cursor.fetchall()
            return results
        except Error as e:
            print(f"Ошибка при получении данных студентов: {e}")
            return []

    def new_person(self,first_name,middle_name,last_name,login,email,status):
        try:
            if not self.connection or not self.connection.is_connected():
                print("Нет подключения к БД")
                return False
            
            if status=="Учитель":
                self.cursor.execute("""SELECT id FROM `Teacher` WHERE first_name = %s AND last_name = %s AND login = %s LIMIT 1""",(first_name,last_name,login))
            else:
                self.cursor.execute("""SELECT id FROM `Student` WHERE first_name = %s AND last_name = %s AND login = %s LIMIT 1""",(first_name,last_name,login))

            result = self.cursor.fetchall()

            if not result:
                password=generate_password(10)
                send_password(password,email,login)
                hashed_password=hash_password(password)
                if middle_name:
                    if status == "Учитель":
                        self.cursor.execute("""INSERT `Teacher`(first_name, middle_name, last_name, login, email, password) VALUES (%s,%s,%s,%s,%s,%s)""",(first_name,middle_name,last_name,login,email,hashed_password))
                    else:
                        self.cursor.execute("""INSERT `Student`(first_name, middle_name, last_name, login, email, password) VALUES (%s,%s,%s,%s,%s,%s)""",(first_name,middle_name,last_name,login,email,hashed_password))
                else:
                    if status == "Учитель":
                        self.cursor.execute("""INSERT `Teacher`(first_name, last_name, login, email, password) VALUES (%s,%s,%s,%s,%s)""",(first_name,last_name,login,email,hashed_password))
                    else:
                        self.cursor.execute("""INSERT `Student`(first_name, last_name, login, email, password) VALUES (%s,%s,%s,%s,%s)""",(first_name,last_name,login,email,hashed_password))

                self.connection.commit()
                return True
            else:
                return False
        except Error as e:
            return False

    def del_person(self,id_for_delete,id_select_status):
        try:
            print(id_for_delete,id_select_status)
            if not self.connection or not self.connection.is_connected():
                print("Нет подключения к БД")
                return False

            if id_select_status == "Учитель":
                self.cursor.execute("""SELECT login FROM `Teacher` WHERE id = %s LIMIT 1""",(int(id_for_delete)))
            else: 
                self.cursor.execute("""SELECT login FROM `Student` WHERE id = %s LIMIT 1""",(int(id_for_delete)))

            result = self.cursor.fetchone()

            print(result)

            if not result:
                print("yes")
            else:
                print("else")
            # if not result:
                # if id_select_status == "Учитель":
                    # self.cursor.execute("""DELETE FROM `Teacher` WHERE id = %s""",(id_for_delete))
                # else:
                    # self.cursor.execute("""DELETE FROM `Student` WHERE id = %s""",(id_for_delete))

                # self.connection.commit()
                # return True
            # else:
                # return False
        except Error as e:
            return False

    def send_biometric(self,id_person,status,url):
        try:
            if status == "Учитель":
                self.cursor.execute("""SELECT id FROM `Teacher` WHERE id = %s LIMIT 1""",(int(id_person),))
            else:
                self.cursor.execute("""SELECT id FROM `Student` WHERE id = %s LIMIT 1""",(int(id_person),))

            if not self.cursor.fetchone():
                print("Пользователь не найден в базе данных")
                return False

            person_image = cv2.imread(url)
            # person_image = cv2.cvtColor(person_image, cv2.COLOR_BGR2RGB)
            face_points = self.detector.points_face(person_image)

            if isinstance(face_points, np.ndarray) and face_points.size == 0:
                print("Лицо не обнаружено на изображении")
                return False
            
            if status == "Учитель":
                filename = f"{id_person}_t.json"
            else:
                filename = f"{id_person}_s.json"

            with open(filename, 'w') as f:
                json.dump(face_points.tolist(), f)

            if not os.path.exists(filename):
                print(f"Файл {filename} не найден.")
                return False

            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            self.client.verify = False

            self.client.upload_file(remote_path=f"face_data/{filename}", local_path=f'D:/DEMO/PHP/Admin_app/{filename}')

            if status == "Учитель":
                self.cursor.execute("""UPDATE `Teacher` SET `Teacher`.face_data = %s WHERE (`Teacher`.id = %s) """,(filename,int(id_person)))
            else:
                print(filename,id_person)
                self.cursor.execute("""UPDATE `Student` SET `Student`.face_data = %s WHERE (`Student`.id = %s) """,(filename,int(id_person)))
            
            os.remove(f'D:/DEMO/PHP/Admin_app/{filename}')
            self.connection.commit()
            return True

        except Error as e:
            return False

    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()

# Face_data_system
# cw4mCk6k0fG7h5iFz0kC