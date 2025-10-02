import dlib
import cv2
from scipy.spatial.distance import pdist
from face_recognition import face_encodings
import numpy as np
from imutils import face_utils

class identification_detector():
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.landmark_predict = dlib.shape_predictor('./src/shape_predictor_68_face_landmarks.dat')
        self.target_size = (640, 480)
        self.encoding_cache = {}

    def points_face(self, img):
        height, width = img.shape[:2]
        if height > self.target_size[1] or width > self.target_size[0]:
            scale = min(self.target_size[0]/width, self.target_size[1]/height)
            img = cv2.resize(img, None, fx=scale, fy=scale)
    
        img_hash = hash(img.tobytes())
        if img_hash in self.encoding_cache:
            return self.encoding_cache[img_hash]

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_rect = self.detector(img_gray, 0)

        if len(face_rect) == 0:
            return None

        encodings = face_encodings(img, known_face_locations=[(f.top(), f.right(), f.bottom(), f.left()) for f in face_rect], num_jitters=1, model="small")
        
        if len(encodings) > 0:
            self.encoding_cache[img_hash] = encodings[0]
            if len(self.encoding_cache) > 100:
                self.encoding_cache.pop(next(iter(self.encoding_cache)))
            return encodings[0]
            
        return None

    def compare_faces(self, known_encoding, face_encoding, tolerance=0.5):
        return np.linalg.norm(known_encoding - face_encoding) <= tolerance
    
    def get_face_landmarks(self, img):
        try:
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            face_rects = self.detector(img_gray, 0)
            if len(face_rects) == 0:
                return None, None
                
            face_rect = face_rects[0]
            landmarks = self.landmark_predict(img_gray, face_rect)
            landmarks = face_utils.shape_to_np(landmarks)

            FACIAL_LANDMARKS_INDEXES = {
                "mouth": (48, 68),
                "right_eyebrow": (17, 22),
                "left_eyebrow": (22, 27),
                "right_eye": (36, 42),
                "left_eye": (42, 48),
                "nose": (27, 35),
                "jaw": (0, 17)
            }
            
            face_regions = {}
            for region, (start, end) in FACIAL_LANDMARKS_INDEXES.items():
                face_regions[region] = landmarks[start:end]
                
            return landmarks, face_regions, face_rect
            
        except Exception as e:
            print(f"Ошибка при поиске ключевых точек: {e}")
            return None, None, None

    def visualize_landmarks(self, img, landmarks, face_rect=None):
        if landmarks is None:
            return img
            
        img_copy = img.copy()
        if face_rect:
            x1, y1 = face_rect.left(), face_rect.top()
            x2, y2 = face_rect.right(), face_rect.bottom()
            cv2.rectangle(img_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        for (x, y) in landmarks:
            cv2.circle(img_copy, (x, y), 2, (0, 0, 255), -1)
            
        return img_copy


