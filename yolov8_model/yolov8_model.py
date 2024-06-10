'''
5/3/2024
Trains an image classification model using YOLO v8
'''

from ultralytics import YOLO
# use a partially pre-trained model
model = YOLO("yolov8n-cls.pt")
# train the model using the data in the split_data folder
model.train(data="/Users/tavis/OneDrive/Desktop/Leaf Identification/split_data", epochs=20, imgsz=64)
