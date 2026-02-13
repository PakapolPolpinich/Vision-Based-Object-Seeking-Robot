from ultralytics import YOLO
import cv2
import os
from spi_to_stm32 import SPIProtocol

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
    "best_ncnn_model"
    )
model_object = YOLO(model_path)

# open camera
cap = cv2.VideoCapture(0)

Width_real = {
    "bicycle": 6.1,
    "tank": 6.6,
    "plane": 4.7,
    "doll": 4.0
}
Focus_real = 512.5
#Distance_real = [0,0,0,0]

# 4 class (your mapping)
key_to_class = {
    ord('b'): "bicycle",
    ord('t'): "tank",
    ord('p'): "plane",
    ord('d'): "doll",
}

target_class = None          # class name that user selected
trigger_predict = False      # run predict only when user presses a key

Set_robot_middle = 0

# ====== TUNING ======
TOL = 20          #  (px)
ALPHA = 0.2       # exponential smoothing (0.15-0.30)
JUMP_TH = 80      # outlier threshold (60-150)
MAX_STEP = 20     # rate limit per frame (10-30)


# ====== STATE (???????? global/??? loop) ======
dx_f = 0.0
dy_f = 0.0
dx_cmd = 0.0
dy_cmd = 0.0
filter_inited = False
center_count = 0
dx_prev = 0
dy_prev = 0
dxdy_inited = False

def find_robot_middle(frame_camera,x1_oj, y1_oj, x2_oj, y2_oj):
    height, width = frame_camera.shape[:2]
    center_x = width // 2
    center_y = height // 2
    object_center_x = (x1_oj + x2_oj) // 2
    object_center_y = (y1_oj + y2_oj) // 2
    dx = object_center_x - center_x
    dy = object_center_y - center_y
    return dx,dy

TOL = 20
spi = SPIProtocol()

found_object = False
object_firsttime = True
centered_found_F = False
count_center = 0

while True:
    check_cap_sucess, frame = cap.read()

    #check status camera
    if check_cap_sucess == True:
        if target_class is not None:
            cv2.putText(frame, f"Target: {target_class} (press b/t/p/d)", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        else:
            cv2.putText(frame, "Press b/t/p/d to detect (q to quit)", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        if trigger_predict == True and target_class is not None:
            results = model_object.predict(frame,imgsz = 512 ,conf=0.7, verbose=False) #return list of results
            # get boxes classes
            boxes = results[0].boxes
            matched = []
            if boxes is not None and len(boxes) > 0:
              
                for i in range(len(boxes)):
                    cls_id = int(boxes.cls[i].item())
                    name = model_object.names[cls_id]
                    if name == target_class:
                        found_object = True
                        if object_firsttime == True:
                             spi.send(b"s")
                             object_firsttime = False

                        x1, y1, x2, y2 = boxes.xyxy[i].cpu().numpy()
                        conf = float(boxes.conf[i].item()) if boxes.conf is not None else 0.0
                        matched.append((conf, (x1, y1, x2, y2)))
                        #find a distance
                        width_Camera_object = y2 - y1
                        distance = (Width_real[name] * Focus_real) / width_Camera_object
                        #move robot to center objectSSS
                       
                        dx, dy = find_robot_middle(frame, x1, y1, x2, y2)
                        
                        # if not dxdy_inited:
                        #     dx_prev, dy_prev = dx, dy
                        #     dxdy_inited = True
                        # else:
                        #     if abs(dx - dx_prev) > 40:
                        #         dx = dx_prev
                        #     if abs(dy - dy_prev) > 40:
                        #         dy = dy_prev

                        #     dx_prev, dy_prev = dx, dy


                        centered = (abs(dx) <= TOL)
                        ##################################
                        
                        # #code move robot to center object
                        if centered == False and count_center < 2:
                            if dx > 0:
                                spi.send(b"r")
                            elif dx < 0:
                                spi.send(b"l")
                        else :
                            spi.send(b"s")
                            count_center += 1
                            #centered_found_F = True

                        ##################################
                        cv2.putText(frame, f"error dx,dy = ({dx},{dy})", (10, 70),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                    (0, 255, 0) if centered else (0, 0, 255), 2)
                        if centered == True:
                            cv2.putText(frame, "Centered!", (10, 90),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                        # print(dx)
            #else motorcontrol to find a match            
            if found_object == False: #check first time
                spi.send(b"c") #clockwise
             
            #print(found_object)
            # draw best match (highest confidence)
            if len(matched) > 0:
                matched.sort(key=lambda x: x[0], reverse=True)
                best_conf, (x1, y1, x2, y2) = matched[0]

                x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                               
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                cv2.putText(frame, f"d: {distance:.2f} cm", (x1, y2 + 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                cv2.putText(frame, f"{target_class} {best_conf:.2f}",
                            (x1, max(0, y1 - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            else:
                cv2.putText(frame, f"Not found: {target_class}", (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)


    cv2.imshow("camera", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        spi.send(b"s")
        break

    # press b/t/m/d -> set target class and trigger predict
    if key in key_to_class:
        target_class = key_to_class[key]
        trigger_predict = True
        found_object = False
        object_firsttime = True
        count_center = 0

cap.release()
cv2.destroyAllWindows()