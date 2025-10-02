import dlib
import cv2
from scipy.spatial.distance import pdist
from face_recognition import face_encodings
import numpy as np
from imutils import face_utils

class identification_detector():
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.landmark_predict = dlib.shape_predictor('./classes/model/shape_predictor_68_face_landmarks.dat')
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
        print(np.linalg.norm(known_encoding - face_encoding))
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


# detector = identification_detector()

# img1 = cv2.imread('../image5.jpg')
# img2 = cv2.imread('../face1.jpg')

# encoding1 = detector.points_face(img1)
# encoding2 = detector.points_face(img2)

# # encoding2 = [-0.09764594584703445, 0.11919991672039032, -0.012743376195430756, -0.03329542651772499, -0.19999729096889496, 0.05182773247361183, -0.04425812140107155, -0.07023162394762039, 0.17480617761611938, -0.10791385173797607, 0.2317948341369629, -0.017751162871718407, -0.2951057255268097, -0.003061909694224596, -0.10974766314029694, 0.1335536688566208, -0.12045760452747345, -0.15521080791950226, -0.04890165850520134, 0.011800769716501236, 0.1258571892976761, 0.044700559228658676, 0.010469218716025352, 0.006348680704832077, -0.07114822417497635, -0.34611985087394714, -0.03718361258506775, -0.04595649242401123, -0.01991979219019413, -0.13555139303207397, -0.033096104860305786, 0.008027259260416031, -0.19762922823429108, -0.02134794183075428, -0.002568153664469719, 0.10256530344486237, -0.11466538906097412, 0.01807578280568123, 0.23165887594223022, 0.025664201006293297, -0.2632482647895813, -0.013126453384757042, 0.010720876045525074, 0.253135621547699, 0.15029045939445496, 0.06575878709554672, -0.046475961804389954, -0.09062277525663376, 0.03899795189499855, -0.23450960218906403, 0.053249530494213104, 0.19247129559516907, 0.10742754489183426, 0.03416801989078522, 0.010119346901774406, -0.12203120440244675, -0.012485709972679615, 0.14155463874340057, -0.1278301626443863, 0.02988610416650772, 0.1074952632188797, -0.17647558450698853, -0.05014827102422714, -0.07452792674303055, 0.22508972883224487, 0.045554544776678085, -0.08166350424289703, -0.18042640388011932, 0.09256405383348465, -0.15925881266593933, -0.13240905106067657, 0.12796708941459656, -0.07662755995988846, -0.21274898946285248, -0.2642365097999573, 0.02060629054903984, 0.4010408818721771, 0.12971968948841095, -0.15314224362373352, 0.015648331493139267, -0.01717142015695572, -0.006919237319380045, 0.13398334383964539, 0.04907489940524101, -0.03722896799445152, 0.02661391720175743, -0.18388992547988892, 0.020245863124728203, 0.2085474133491516, -0.089258573949337, -0.05685737729072571, 0.20406009256839752, -0.00401106383651495, 0.1064680889248848, 0.03832308202981949, 0.040691077709198, -0.03910698741674423, 0.02645362913608551, -0.14466384053230286, -0.04598042741417885, 0.06721372902393341, -0.06949052959680557, -0.021746529266238213, 0.06473106890916824, -0.11579864472150803, 0.07546073198318481, -0.04414167255163193, 0.012874110601842403, -0.015479659661650658, -0.053484413772821426, -0.15062063932418823, -0.03813111409544945, 0.1713985651731491, -0.2594936490058899, 0.23842430114746094, 0.15851041674613953, 0.028129015117883682, 0.11263997107744217, 0.17247475683689117, 0.017556075006723404, -0.007283017970621586, -0.0748637318611145, -0.24425406754016876, -0.06683014333248138, 0.10113532841205597, -0.004392350558191538, 0.13234774768352509, 0.0003054151311516762]
# if encoding1 is not None and encoding2 is not None:
#     is_match = detector.compare_faces(encoding1, encoding2)
#     print(f"Лица совпадают: {is_match}")

# img = cv2.imread('159260184.jfif')

# landmarks, face_regions, face_rect = detector.get_face_landmarks(img)

# if landmarks is not None:
#     left_eye = face_regions["left_eye"]
#     right_eye = face_regions["right_eye"]
#     mouth = face_regions["mouth"]
    
#     result_img = detector.visualize_landmarks(img, landmarks, face_rect)
#     cv2.imshow("Landmarks", result_img)
#     cv2.waitKey(0)


