from ultralytics import YOLO
import os


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
model_path = os.path.join(
    ROOT,
    "train",
    "vision",
    "run_Ncnn",
    "best.pt"
    )

model = YOLO(model_path)
model.export(format="ncnn", imgsz=512, half=False)
print("done")
