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

cap = VideoStream(src=1).start()

real_detected_time = 0
penalty_time = 0
blink_time = 0

type_detect=""
procent_detect=0

count_faces = 0
count_frame=0
total=0

test1=LiveDetect_class.liveness_detection()
test2=BlinkEyes_class.eye_blink_detector()

test_bonus1 = CountFace_class.count_faces()
test_bonus2 = ObjectDetect_class.object_detect()

db = ConnectionDB.check_face_db("60")
final = Identification_face.identification_detector()

step1=True
step2=False
step3=False
step4=False
step5=False

count_first = 0
count_second = 0

real_detect = False

frame_buffer = np.zeros((5,), dtype=np.uint8)
frame_idx = 0

if db.connect():
    while True:

        img = cap.read()
        if img is None:
            continue

        img = cv2.flip(img,1)

        scale = 0.9
        img = cv2.resize(img, None, fx=scale, fy=scale)
        img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        if count_frame % 2 == 0:

            count_first = test_bonus1.count_the_number_of_faces_haarcascade(img_gray)
            count_second = test_bonus1.count_the_number_of_faces_dlib(img_gray)

            # print(count_first,count_second)

            if count_first == 1 and count_second == 1:
                # cell_phone1 = test_bonus2.cell_phone_detector_second(img)
                cell_phone = test_bonus2.cell_phone_detector(img)
            else:
                cell_phone = False

        current_time = time.time()
        if (count_first >= 2 and count_second >=2) or ((count_first == 0 and count_second == 0)):
            step1 = step2 = step3 = step4 = False
            penalty_time = current_time
        elif not cell_phone and ((current_time - penalty_time) > 5.0) and not real_detect:
            step1 = True
            db.get_number_pair()
            
        if step1 and count_frame % 2 == 0:
            step2 = step3 = False
            type_detect, procent_detect = test1.detector(img)
            if (type_detect == "real") and (procent_detect >= 0.8):
                if real_detected_time == 0:
                    real_detected_time = time.time()
                elif (time.time() - real_detected_time) > 5.0:
                    step1 = False
                    step2 = True
                    real_detect = True
            elif (type_detect == "spoof"):
                print("spoof face")
                real_detected_time = 0
                step1 = True
                real_detect = False
            else:
                print("unknown face")
                real_detected_time = 0

        if step2 and count_frame % 2 == 0:
            step1 = step3 = False
            faces = test2.detector(img_gray)
            for face in faces:
                count_frame,total= test2.eye_blink(img_gray,face,count_frame,total)

                frame_buffer[frame_idx] = 1 if total > frame_buffer[frame_idx-1] else 0
                frame_idx = (frame_idx + 1) % 5

                recent_blinks = np.sum(frame_buffer)

                if recent_blinks >= 4:
                    print("blink detect")
                    step2=False
                    step3=True
                    total=0
                    count_frame=0
                    frame_buffer.fill(0)
                    frame_idx = 0

        if step3 and count_frame % 2 == 0:
            step1 = step2 = step3 = False
            db.get_student_list()
            if not db.dict_stud:
                print("Нету студентов")
                step1 = step2 = step3 = step4 = step5 = False
            else:
                step4 = True
        
        if step4 and count_frame % 2 == 0:
            person_face = final.points_face(img)
            step1 = step2 = step3 = step4 = False
            step5 = True

        if step5 and count_frame % 2 == 0:
            for key, value in db.dict_stud.items():
                if person_face is not None and value is not None:
                    res = final.compare_faces(person_face,value)
                    if res:
                        print(key,"-",value)
                        db.attendance_student(key)
            step2 = step3 = step4 = step5 = False
            step1 = True

        count_frame += 1
        
        if count_frame % 2 == 0:
            cv2.imshow("image", img)

        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break

cap.release()
cv2.destroyAllWindows() 