from ultralytics import YOLO
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(script_dir, "data.yaml")
project_root = os.path.dirname(script_dir)

model = YOLO('./yolov8n.pt')

model.train(data=data_file, epochs=100, batch=16, imgsz=640, project=project_root, name='train_beta')
metrics = model.val()