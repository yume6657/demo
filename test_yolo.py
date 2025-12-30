from ultralytics import YOLO
import cv2

model = YOLO("weights/license_plate_detector.pt")

img = cv2.imread("test.jpg")  # 放一张车牌图片
results = model(img)

results[0].show()

