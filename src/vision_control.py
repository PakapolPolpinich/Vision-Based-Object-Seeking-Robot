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

cap = cv2.VideoCapture(0)

Width_Real = [5.8,0,0,0] # cm

while True:
    check_cap_sucess, frame = cap.read()
    #check status camera
    if check_cap_sucess == True:
        
        results = model_object.predict(frame, conf=0.4, verbose=False) #return list of results

        # get boxes classes
        boxes = results[0].boxes
        # show result
        annotated = results[0].plot()
        if boxes is not None:
            for box in boxes:
                # class id
                cls_id = int(box.cls[0])

                #  class name
                class_name = model_object.names[cls_id]

                # bounding box
                x1, y1, x2, y2 = box.xyxy[0]

                print(f"Class: {class_name}")
                print(f"Box: x1={x1:.1f}, y1={y1:.1f}, x2={x2:.1f}, y2={y2:.1f}")
                print("-----")
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                text = f"{class_name} x1:{x1} y1:{y1} x2:{x2} y2:{y2}"
                #text_y = y1 - 10 if y1 - 10 > 10 else y1 + 20

                w = y2 - y1
                W = 5.8
                # d = 20.5
                # f = (w * d) / W

                f = 512.5  #focal length
                d = (W * f) / w
                # cv2.putText(
                #     annotated, f"f: {f:.2f} pixel", (x1, y2 + 20),
                #     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2
                # )
                cv2.putText(
                    annotated, f"d: {d:.2f} cm", (x1, y2 + 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2
                )
                # cv2.putText(
                #     annotated, text, (x1, y2),
                #     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2
                # )

                cv2.circle(annotated, (x1, y1), 4, (0, 0, 255), -1)   # top-left
                cv2.circle(annotated, (x2, y2), 4, (255, 0, 0), -1)   # bottom-right
      
        cv2.imshow("Vision", annotated)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        print("Cannot open camera")
        break

cap.release()
cv2.destroyAllWindows()