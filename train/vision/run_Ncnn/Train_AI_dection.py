import torch
from ultralytics import YOLO
import multiprocessing

def check_device():
    print("===== DEVICE CHECK =====")
    if torch.cuda.is_available():
        print(f"GPU detected: {torch.cuda.get_device_name(0)}")
        print(f"CUDA Version: {torch.version.cuda}")
    else:
        print(" GPU not available, using CPU")

def train_model():
    print("===== LOAD MODEL =====")
    model = YOLO("yolov8n.pt") 

    print("===== START TRAINING =====")
    results = model.train(
        data=r"C:\Users\usEr\Documents\networkandNeural\Project_Neural\object-toy-1\data.yaml",#path dataset
        epochs=200,
        imgsz=512,
        batch=8,
        device=0 if torch.cuda.is_available() else "cpu",
        workers=0,              
        cache=False,
        name="Object_detection_for_robot_v7(200)",
        pretrained=True
    )

    print("===== TRAIN COMPLETE =====")
    return model


def export_ncnn(model):
    print("===== EXPORT TO NCNN =====")
    model.export(format="ncnn")
    print("===== EXPORT COMPLETE =====")


def main():
    check_device()
    model = train_model()
    export_ncnn(model)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
