from ultralytics import YOLO
import cv2
import os


# path model
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
model_path = os.path.join(
    ROOT,
    "train",
    "vision",
    "runs",
    "detect",
    "result_vision",
    "Result",
    "weights",
    "best.pt"
    )
model_object = YOLO(model_path)

model_object.export(format = "ncnn",imgsz = 512)
