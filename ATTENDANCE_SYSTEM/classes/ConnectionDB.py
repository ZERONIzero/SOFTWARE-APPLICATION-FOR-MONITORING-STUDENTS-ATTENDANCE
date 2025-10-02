import mysql.connector
from mysql.connector import Error
from datetime import datetime
import json
from webdav3.client import Client
import os, shutil

def clear_directory(directory_path):
    if os.path.exists(directory_path):
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Ошибка при удалении {file_path}: {e}")
    else:
        print(f"Директория {directory_path} не существует.")

def load_json_files_to_dict(directory_path):
    json_dict = {}
    
    if os.path.exists(directory_path):
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path) and filename.endswith('.json'):
                try:
                    key = filename.split("_")[0]
                    with open(file_path, 'r', encoding='utf-8') as json_file:
                        json_data = json.load(json_file)
                        json_dict[key] = json_data
                except Exception as e:
                    print(f"Ошибка при чтении файла {filename}: {e}")
    else:
        print(f"Директория {directory_path} не существует.")
    
    return json_dict

class check_face_db():
    def __init__(self, room : str):
        self.config = {
            'host' : "s-3.h.filess.io",
            'database' : "Exam_socialsign",
            'password' : "7fc55fb542161bb01fa3cc3d6f5f96593ebb4962",
            'username' : "Exam_socialsign",
            'port' : "3307",
        }
        self.webdav_config = Client({
            'webdav_hostname': "https://webdav.cloud.mail.ru",
            'webdav_login': "Brandodio9@mail.ru",
            'webdav_password':"cw4mCk6k0fG7h5iFz0kC"
        })
        self.audience = room
        self.connection = None
        self.number_pair = None
        self.current_time = None
        self.cursor = None
        self.today = None
        self.id_schedule = None
        self.timepair_list = []
        self.dict_stud = None

    def connect(self) -> bool:
        try:
            self.connection = mysql.connector.connect(**self.config)
            if self.connection.is_connected():
                print("Есть подключения")
                self.cursor = self.connection.cursor()
                self.cursor.execute("SELECT CONCAT(start_pair,'-',end_pair) FROM `Timepair`")
                results = self.cursor.fetchall()
                if results:
                    for time_range in results:
                        tt = time_range[0].split("-")

                        start_time = tt[0][:-3]
                        start_time = datetime.strptime(start_time,'%H:%M')
                        start_time_seconds = round((start_time - start_time.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds())

                        end_time = tt[1][:-3]
                        end_time = datetime.strptime(end_time,'%H:%M')
                        end_time_seconds = round((end_time - end_time.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds())
                        self.timepair_list.append(str(str(start_time_seconds)+"-"+str(end_time_seconds)))
                        print(self.timepair_list)

                else:
                    print("Невозможно получить с бд график времени занятий")
                return True
        except Error as e:
            print("Нету подключения")
            return False

    def get_number_pair(self):
        now = datetime.now()
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        self.current_time = round((now - start_of_day).total_seconds())

        if self.timepair_list:
            count = 0
            for count_pair in self.timepair_list:
                tt = count_pair.split("-")
                start_time = tt[0]
                end_time = tt[1]
                if (int(start_time)-120) <= int(self.current_time) < (int(end_time)):
                    self.number_pair=count+1
                    print(self.number_pair)
                    return
                else:
                    self.number_pair=None
                    count+=1
            print("Сейчас переменна",self.number_pair)
            return
        else:
            print("Нету данных в timepair_list")
            return


    def get_student_list(self):
        if self.connection.is_connected():
            self.today = datetime.now().strftime("%Y-%m-%d")
            self.cursor.execute(""" SELECT id, `Schedule`.group FROM `Schedule` WHERE room = %s AND date = %s AND number_pair = %s LIMIT 1""",(self.audience, self.today, self.number_pair))

            result = self.cursor.fetchone()

            if not result:
                print(f"Занятия в {self.audience} аудитории {self.today} числа на {self.number_pair} паре не найден")
                return False
            else:
                self.id_schedule , group_id = result
                self.cursor.execute("""SELECT student_code FROM `Students_in_group` WHERE group_code = %s """,(group_id,))
                stud_id_list = self.cursor.fetchall()
                print(stud_id_list, self.id_schedule)
                if not stud_id_list:
                    print("Нету студентов в данной группе")

                clear_directory("./face_data_stud")
                for id_count, in stud_id_list:
                    self.webdav_config.download_sync(remote_path=f"face_data/{str(id_count)}_s.json", local_path=f"./face_data_stud/{str(id_count)}_s.json")

                self.dict_stud = load_json_files_to_dict("./face_data_stud")
                clear_directory("./face_data_stud")

                
    def attendance_student(self,id_stud):
        if self.connection.is_connected():
            self.cursor.execute("""SELECT id FROM `Attendance` WHERE student_id = %s AND schedule_id = %s LIMIT 1""",(id_stud,self.id_schedule))

            result = self.cursor.fetchone()
            if not result:
                self.cursor.execute("""INSERT `Attendance`(student_id, schedule_id) VALUES (%s, %s)""",(id_stud,self.id_schedule))
                self.connection.commit()
