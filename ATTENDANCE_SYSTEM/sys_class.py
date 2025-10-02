import cv2
import scipy.spatial.distance as dist 
from imutils import face_utils
from imutils.video import VideoStream
import time
import numpy as np

from classes import BlinkEyes_class
from classes import LiveDetect_class
from classes import CountFace_class
from classes import ObjectDetect_class
from classes import ConnectionDB
from classes import Identification_face

class FaceRecognitionSystem:
    def __init__(self, video_source, room_name):
        self.cap = VideoStream(src=video_source).start()
        self.real_detected_time = 0
        self.penalty_time = 0
        self.blink_time = 0
        self.type_detect = ""
        self.procent_detect = 0
        self.count_faces = 0
        self.count_frame = 0
        self.total = 0
        self.test1 = LiveDetect_class.liveness_detection()
        self.test2 = BlinkEyes_class.eye_blink_detector()
        self.test_bonus1 = CountFace_class.count_faces()
        self.test_bonus2 = ObjectDetect_class.object_detect()
        self.db = ConnectionDB.check_face_db(room_name)
        self.final = Identification_face.identification_detector()
        self.step1 = True
        self.step2 = False
        self.step3 = False
        self.step4 = False
        self.step5 = False
        self.count_first = 0
        self.count_second = 0
        self.real_detect = False
        self.frame_buffer = np.zeros((5,), dtype=np.uint8)
        self.frame_idx = 0

    def run(self):
        if self.db.connect():

            # if not self.cap.isOpened():
            #     print("Ошибка: Не удалось открыть камеру.")
            #     return

            while True:
                img = self.cap.read()
                if img is None:
                    continue

                img = cv2.flip(img, 1)
                scale = 0.9
                img = cv2.resize(img, None, fx=scale, fy=scale)
                img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                if self.count_frame % 2 == 0:
                    self.process_frame(img_gray, img)

                self.count_frame += 1

                if self.count_frame % 2 == 0:
                    cv2.imshow("image", img)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        self.cap.release()
        cv2.destroyAllWindows()

    def process_frame(self, img_gray, img):
        current_time = time.time()

        self.count_first = self.test_bonus1.count_the_number_of_faces_haarcascade(img_gray)
        self.count_second = self.test_bonus1.count_the_number_of_faces_dlib(img_gray)

        if self.count_first == 1 and self.count_second == 1:
            cell_phone = self.test_bonus2.cell_phone_detector(img)
        else:
            cell_phone = False

        if (self.count_first >= 2 and self.count_second >= 2) or ((self.count_first == 0 and self.count_second == 0)):
            print('Найден телефон')
            self.step1 = self.step2 = self.step3 = self.step4 = False
            self.penalty_time = current_time
        elif not cell_phone and ((current_time - self.penalty_time) > 5.0) and not self.real_detect:
            self.step1 = True
            self.db.get_number_pair()

        if self.step1 and self.count_frame % 2 == 0:
            self.handle_step1(img)

        if self.step2 and self.count_frame % 2 == 0:
            self.handle_step2(img_gray)

        if self.step3 and self.count_frame % 2 == 0:
            self.handle_step3()

        if self.step4 and self.count_frame % 2 == 0:
            self.handle_step4(img)

        if self.step5 and self.count_frame % 2 == 0:
            self.handle_step5()

    def handle_step1(self, img):
        self.step2 = self.step3 = False
        self.type_detect, self.procent_detect = self.test1.detector(img)
        if (self.type_detect == "real") and (self.procent_detect >= 0.8):
            if self.real_detected_time == 0:
                self.real_detected_time = time.time()
            elif (time.time() - self.real_detected_time) > 5.0:
                self.step1 = False
                self.step2 = True
                self.real_detect = True
        elif (self.type_detect == "spoof"):
            print("spoof face")
            self.real_detected_time = 0
            self.step1 = True
            self.real_detect = False
        else:
            print("unknown face")
            self.real_detected_time = 0

    def handle_step2(self, img_gray):
        self.step1 = self.step3 = False
        faces = self.test2.detector(img_gray)
        for face in faces:
            self.count_frame, self.total = self.test2.eye_blink(img_gray, face, self.count_frame, self.total)
            self.frame_buffer[self.frame_idx] = 1 if self.total > self.frame_buffer[self.frame_idx - 1] else 0
            self.frame_idx = (self.frame_idx + 1) % 5
            recent_blinks = np.sum(self.frame_buffer)

            if recent_blinks >= 4:
                print("blink detect")
                self.step2 = False
                self.step3 = True
                self.total = 0
                self.count_frame = 0
                self.frame_buffer.fill(0)
                self.frame_idx = 0

    def handle_step3(self):
        self.step1 = self.step2 = self.step3 = False
        self.db.get_student_list()
        if not self.db.dict_stud:
            print("Нету студентов")
            self.step1 = self.step2 = self.step3 = self.step4 = self.step5 = False
        else:
            self.step4 = True

    def handle_step4(self, img):
        self.person_face = self.final.points_face(img)
        self.step1 = self.step2 = self.step3 = self.step4 = False
        self.step5 = True

    def handle_step5(self):
        min_val = 0.0
        student_key = None
        for key, value in self.db.dict_stud.items():
            if self.person_face is not None and value is not None:
                res = self.final.compare_faces(self.person_face, value)
                if res:
                    if res >= 0.7:
                        if min_val < res:
                            min_val = res
                            student_key = key
        print(student_key, "-", min_val)
        if student_key:
            self.db.attendance_student(student_key)
        self.step2 = self.step3 = self.step4 = self.step5 = False
        self.step1 = True

if __name__ == "__main__":
    face_recognition_system = FaceRecognitionSystem(1,"60")
    face_recognition_system.run()