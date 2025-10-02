import dlib
from imutils import face_utils
from scipy.spatial import distance as dist
import time
import cv2

class eye_blink_detector():

    def __init__(self):
        self.blink_thresh = 0.2
        self.succ_frame = 4
        self.detector = dlib.get_frontal_face_detector()
        self.landmark_predict= dlib.shape_predictor('./classes/model/shape_predictor_68_face_landmarks.dat')
        self.last_blink_time = 0
        self.min_blink_interval = 2.0

    def calculate_EAR(self,eye): 
        y1 = dist.euclidean(eye[1], eye[5]) 
        y2 = dist.euclidean(eye[2], eye[4])    
        x1 = dist.euclidean(eye[0], eye[3]) 
        if x1 > 0:
            return (y1+y2) / (x1*2.0)
        else:
            return 0 
    
    def eye_blink(self,img_gray,face,count_frame,total):
        current_time = time.time()

        (L_start, L_end) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"] 
        (R_start, R_end) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']

        shape = self.landmark_predict(img_gray, face) 
        shape = face_utils.shape_to_np(shape) 
 
        lefteye = shape[L_start: L_end]
        righteye = shape[R_start:R_end] 

        left_EAR = self.calculate_EAR(lefteye) 
        right_EAR = self.calculate_EAR(righteye) 
        avg = (left_EAR + right_EAR)/2.0

        if avg < self.blink_thresh: 
            count_frame += 1 
        else: 
            if (count_frame >= self.succ_frame and (current_time - self.last_blink_time) >= self.min_blink_interval):
                total+=1
                self.last_blink_time = current_time
            count_frame = 0
        
        return count_frame,total












# import cv2
# import dlib
# from imutils import face_utils
# from scipy.spatial import distance as dist
# import time

# class eye_blink_detector():

#     def __init__(self):
#         self.blink_thresh = 0.2
#         self.succ_frame = 4
#         self.detector = dlib.get_frontal_face_detector()
#         self.landmark_predict = dlib.shape_predictor('./model/shape_predictor_68_face_landmarks.dat')
#         self.last_blink_time = 0
#         self.min_blink_interval = 2.0

#     def calculate_EAR(self, eye): 
#         y1 = dist.euclidean(eye[1], eye[5]) 
#         y2 = dist.euclidean(eye[2], eye[4])    
#         x1 = dist.euclidean(eye[0], eye[3]) 
#         if x1 > 0:
#             return (y1 + y2) / (x1 * 2.0)
#         else:
#             return 0 
    
#     def draw_eye_landmarks(self, img, shape):
#         # Рисуем точки на глазах
#         for (x, y) in shape:
#             cv2.circle(img, (x, y), 2, (0, 255, 0), 1)  # Зеленый цвет для точек

#     def eye_blink(self, img_gray, frame, face, count_frame, total):
#         current_time = time.time()

#         (L_start, L_end) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"] 
#         (R_start, R_end) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']

#         shape = self.landmark_predict(img_gray, face)
#         print(shape) 
#         shape = face_utils.shape_to_np(shape)
#         print(shape) 

#         lefteye = shape[L_start: L_end]
#         # print(L_start,L_end)
#         righteye = shape[R_start:R_end]
#         # print(R_start,R_end) 

#         # Отображаем точки глаз на изображении
#         self.draw_eye_landmarks(frame, lefteye)  # Рисуем точки левого глаза
#         self.draw_eye_landmarks(frame, righteye)  # Рисуем точки правого глаза

#         left_EAR = self.calculate_EAR(lefteye) 
#         right_EAR = self.calculate_EAR(righteye) 
#         avg = (left_EAR + right_EAR) / 2.0

#         if avg < self.blink_thresh: 
#             count_frame += 1 
#         else: 
#             if (count_frame >= self.succ_frame and (current_time - self.last_blink_time) >= self.min_blink_interval):
#                 total += 1
#                 self.last_blink_time = current_time
#             count_frame = 0
        
#         return count_frame, total

# Основной код для запуска
# if __name__ == "__main__":
#     cap = cv2.VideoCapture(0)  # Используйте 0 для веб-камеры
#     detector = eye_blink_detector()
#     count_frame = 0
#     total_blinks = 0

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         faces = detector.detector(img_gray, 0)

#         for face in faces:
#             count_frame, total_blinks = detector.eye_blink(img_gray, face, count_frame, total_blinks)

#         cv2.putText(frame, f"Blinks: {total_blinks}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
#         cv2.imshow("Eye Blink Detector", frame)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()