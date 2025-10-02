import cv2
import numpy as np

class face_orientation():
    def __init__(self):
        self.frontal=cv2.CascadeClassifier('./classes/model/haarcascade_frontalface_alt.xml')
        self.perfil=cv2.CascadeClassifier('./classes/model/haarcascade_profileface.xml')


    def detect(self,img, cascade):
        rects,_,confidence = cascade.detectMultiScale3(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30),flags=cv2.CASCADE_SCALE_IMAGE, outputRejectLevels = True)
        if len(rects) == 0:
            return (),()
        rects[:,2:] += rects[:,:2]
        return rects,confidence


    def convert_rightbox(self,img,box_right):
        res = np.array([])
        _,x_max = img.shape
        for box_ in box_right:
            box = np.copy(box_)
            box[0] = x_max-box_[2]
            box[2] = x_max-box_[0]
            if res.size == 0:
                res = np.expand_dims(box,axis=0)
            else:
                res = np.vstack((res,box))
        return res


    def bounding_box(self,img,box,match_name=[]):
        for i in np.arange(len(box)):
            x0,y0,x1,y1 = box[i]
            img = cv2.rectangle(img,
                        (x0,y0),
                        (x1,y1),
                        (0,255,0),3);
            if not match_name:
                continue
            else:
                cv2.putText(img, match_name[i], (x0, y0-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)
        return img
    

    def face_orientation(self,gray):
        box_frontal,w_frontal = self.detect(gray,self.frontal)
        if len(box_frontal)==0:
            box_frontal=[]
            name_frontal = []
        else:
            name_frontal = len(box_frontal)*["frontal"]

        box_left,w_left = self.detect(gray,self.perfil)
        if len(box_left)==0:
            box_left = []
            name_left= []
        else:
            name_left = len(box_left)*["left"]

        gray_flipped = cv2.flip(gray,1)
        box_right , w_right = self.detect(gray_flipped,self.perfil)
        if len(box_right)==0:
            box_right = []
            name_right = []
        else:
            box_right = self.convert_rightbox(gray,box_right)
            name_right = len(box_right)*["right"]
        
        boxes = list(box_frontal)+list(box_left)+list(box_right)
        names = list(name_frontal)+list(name_left)+list(name_right)
        return boxes,names