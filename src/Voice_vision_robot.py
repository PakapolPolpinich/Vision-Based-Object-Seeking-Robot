from ultralytics import YOLO
import cv2
import os
from spi_to_stm32 import SPIProtocol
from voiceSTT import VoiceSTT
import time

# ===== STT thread control (NEW) =====
import threading
import queue

STATE = "Audio_detect"

# State sound ====================================================================

VOICE_TO_CLASS = {
    "จักรยาน": "bicycle",
    "รถถัง": "tank",
    "เครื่องบิน": "plane",
    "ตุ๊กตา": "doll",
}

# State vision ====================================================================
target_class = None          # class name that user selected
trigger_predict = False      # run predict only when user presses a key

# path model
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# model_path = os.path.join(
#     ROOT,
#     "train",
#     "vision",
#     "runs",
#     "detect",
#     "result_vision",
#     "Result",
#     "weights",
#     "best_ncnn_model"
# )
model_path = os.path.join(
    ROOT,
    "train",
    "vision",
    "run_Ncnn",
    "best_ncnn_model"
)

# Clockwise to find object
found_object = False
object_firsttime = True

# TUNING center
RATE_R = 900.0   # px/s (turn right) for log
RATE_L = 900.0

MIN_DT = 0.01    # 10ms
MAX_DT = 0.06    # 60ms
TOL = 40         # px (tolerance for being "centered")

count_center = 0
middle_complete = False
destination_reached = False

# distance value
Width_real = {
    "bicycle": 6.1,
    "tank": 6.6,
    "plane": 4.7,
    "doll": 4.0
}
Focus_real = 512.5


def find_robot_middle(frame_camera, x1_oj, y1_oj, x2_oj, y2_oj):
    height, width = frame_camera.shape[:2]
    center_x = width // 2
    center_y = height // 2
    object_center_x = (x1_oj + x2_oj) // 2
    object_center_y = (y1_oj + y2_oj) // 2
    dx = object_center_x - center_x
    dy = object_center_y - center_y
    return dx, dy

# end vision ====================================================================


# ============================ start program ========================================================= #

cap = cv2.VideoCapture(0)  # open camera
spi = SPIProtocol()
model_object = YOLO(model_path)  # load model
stt = VoiceSTT(duration=3.0)  # Initialize STT

# ================================================================================================ #


while True:
    check_cap_sucess, frame = cap.read()
    if not check_cap_sucess:
        continue

    if STATE == "Audio_detect":
        if STATE == "Audio_detect":
            cv2.putText(frame, "STATE: Audio_detect (listening...)", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        text = stt.listen()
        if text:
            print("STT:", text)
            t = text.lower()

            selected = None
            for key_word, cls in VOICE_TO_CLASS.items():
                if key_word in t:
                    selected = cls
                    break

            if selected is not None:
                target_class = selected
                print("Target set to:", target_class)
                trigger_predict = True
                STATE = "Vision_detect"
            else:
                print("No valid target in speech.")

    elif STATE == "Vision_detect":
        # ===== pause STT in Vision_detect so NCNN can use CPU =====

        # (No STT work here -> vision can use CPU)
        cv2.putText(frame, "STATE: Vision", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        if trigger_predict == True and target_class is not None:
            results = model_object.predict(frame, imgsz=512, conf=0.6, verbose=False)  # return list of results

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

                        # move robot to center object
                        dx, dy = find_robot_middle(frame, x1, y1, x2, y2)

                        centered = (abs(dx) <= TOL)
                        ##################################
                        if middle_complete == False:
                            if abs(dx) <= TOL:
                                spi.send(b"s")
                                count_center += 1
                                if count_center > 30:
                                    middle_complete = True
                            else:
                                count_center = 0
                                dx1 = dx
                                if dx > 0:
                                    direction = b"r"
                                    rate = RATE_R
                                else:
                                    direction = b"l"
                                    rate = RATE_L
                                # 3) cal movement dx/rate ( clamp)
                                dt = abs(dx) / rate
                                dt = max(MIN_DT, min(dt, MAX_DT))

                                # 4) send → delay → stop
                                spi.send(direction)
                                time.sleep(float(dt))
                                spi.send(b"s")

                            if centered == True:
                                cv2.putText(frame, "Centered!", (10, 90),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

                        if middle_complete == True:
                            # find a distance
                            width_Camera_object = y2 - y1
                            distance = (Width_real[name] * Focus_real) / width_Camera_object

                            if distance > 20.0 and destination_reached == False:
                                spi.send(b"f")
                            else:
                                spi.send(b"s")
                                destination_reached = True
                                STATE = "IDLE"
                            

        if found_object == False:  # check first time
            spi.send(b"c")  # clockwise

        # draw best match (highest confidence)
        if len(matched) > 0:
            matched.sort(key=lambda x: x[0], reverse=True)
            best_conf, (x1, y1, x2, y2) = matched[0]
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            if middle_complete == True:
                cv2.putText(frame, f"d: {distance:.2f} cm", (x1, y2 + 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(frame, f"{target_class} {best_conf:.2f}",
                        (x1, max(0, y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        else:
            cv2.putText(frame, f"Not found: {target_class}", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    elif STATE == "IDLE":
        cv2.putText(frame, "STATE: IDLE (reset -> audio)", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        # Reset variables for next round
        trigger_predict = True
        found_object = False
        object_firsttime = True
        count_center = 0
        middle_complete = False
        destination_reached = False

        STATE = "Audio_detect"
        print("go to this")
        # (Audio thread will resume automatically in Audio_detect)

    cv2.imshow("camera", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        spi.send(b"s")
        break

cap.release()
cv2.destroyAllWindows()
