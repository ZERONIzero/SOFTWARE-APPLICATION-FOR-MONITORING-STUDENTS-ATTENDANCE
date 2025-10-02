from model_live import LivenessNet
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from keras.utils.np_utils import to_categorical
from imutils import paths
import numpy as np
import argparse
import pickle
import cv2
import os

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
	help="Путь к входным данным (изображениям)")
ap.add_argument("-m", "--model", type=str, required=True,
	help="Путь для обученной модели")
ap.add_argument("-l", "--le", type=str, required=True,
	help="Путь к label encoder")
args = vars(ap.parse_args())

INIT_LR = 1e-4
BS = 8
EPOCHS = 100

print("[INFO] Загрузка изображений...")
imagePaths = list(paths.list_images(args["dataset"]))
data = []
labels = []

for imagePath in imagePaths:
	
	labels.append(imagePath.split(os.path.sep)[-2])
	image = cv2.imread(imagePath)
	image = cv2.resize(image, (32, 32))

	data.append(image)
	

data = np.array(data, dtype="float") / 255.0

le = LabelEncoder()
labels = to_categorical(le.fit_transform(labels), 2)

(trainX, testX, trainY, testY) = train_test_split(data, labels,
	test_size=0.25, random_state=42)

print("[INFO] Компиляция модели...")
opt = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)
model = LivenessNet.build(width=32, height=32, depth=3,
	classes=len(le.classes_))
model.compile(loss="binary_crossentropy", optimizer=opt,
	metrics=["accuracy"])

aug = ImageDataGenerator(rotation_range=20, zoom_range=0.15,
	width_shift_range=0.2, height_shift_range=0.2, shear_range=0.15,
	horizontal_flip=True, fill_mode="nearest")

print("[INFO] Номер прохода {} ".format(EPOCHS))
H = model.fit(x=aug.flow(trainX, trainY, batch_size=BS),
	validation_data=(testX, testY), steps_per_epoch=len(trainX) // BS,
	epochs=EPOCHS)

print("[INFO] Оценка эффективности...")
predictions = model.predict(testX, batch_size=BS)
print(classification_report(testY.argmax(axis=1),
	predictions.argmax(axis=1), target_names=le.classes_))

print("[INFO] Сохранение модели в формате '{}'...".format(args["model"]))
model.save(args["model"], save_format="h5")

f = open(args["le"], "wb")
f.write(pickle.dumps(le))
f.close()

