from ultralytics import YOLO
import cv2
import os
from spi_to_stm32 import SPIProtocol
import time

# ===============================
# MODEL PATH (ตามไฟล์คุณ)
# ===============================
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

# ===============================
# CAMERA
# ===============================
cap = cv2.VideoCapture(0)

# ===============================
# DISTANCE PARAMS (ของเดิม)
# ===============================
Width_real = {
    "bicycle": 6.1,
    "tank": 6.6,
    "plane": 4.7,
    "doll": 4.0
}
Focus_real = 512.5

# ===============================
# KEY -> CLASS (ของเดิม)
# ===============================
key_to_class = {
    ord('b'): "bicycle",
    ord('t'): "tank",
    ord('p'): "plane",
    ord('d'): "doll",
}

target_class = None
trigger_predict = False

# ===============================
# CONTROL TUNING
# ===============================
TOL = 10                # px tolerance (คุณใช้ 50)
MIN_DT = 0.01           # 10ms
MAX_DT = 0.06           # 60ms (ลดจาก 80ms เพื่อกัน overshoot)
CAL_PAUSE = 0.08        # รอภาพนิ่งก่อนวัด dx2 (80ms)

# สำหรับ calibration quality
DPX_MIN = 15            # dpx ต่ำกว่านี้ไม่เอามาคิด rate (กัน noise)
RATE_MIN = 80
RATE_MAX = 900
RATE_ALPHA = 0.25       # smooth rate

spi = SPIProtocol()

# ===============================
# HELPERS
# ===============================
def clamp(x, lo, hi):
    return lo if x < lo else hi if x > hi else x

def find_robot_middle(frame_camera, x1_oj, y1_oj, x2_oj, y2_oj):
    height, width = frame_camera.shape[:2]
    center_x = width // 2
    center_y = height // 2
    object_center_x = (x1_oj + x2_oj) // 2
    object_center_y = (y1_oj + y2_oj) // 2
    dx = object_center_x - center_x
    dy = object_center_y - center_y
    return dx, dy

# ===============================
# STATES
# ===============================
found_object = False
object_firsttime = True

# --- calibration state machine ---
cal_state = 0       # 0=idle, 1=turning, 2=wait+measure
cal_dx1 = 0.0
cal_t1 = 0.0
cal_t2 = 0.0
cal_dir = b"s"
cal_dt = 0.08       # เริ่มต้น (จะถูกปรับอัตโนมัติเมื่อมี rate)
rate_r = None       # px/s (หมุนขวา)
rate_l = None       # px/s (หมุนซ้าย)

# ===============================
# MAIN LOOP
# ===============================
while True:
    check_cap_sucess, frame = cap.read()
    if not check_cap_sucess:
        continue

    # UI text
    if target_class is not None:
        cv2.putText(frame, f"Target: {target_class} (press b/t/p/d)", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    else:
        cv2.putText(frame, "Press b/t/p/d to detect (q to quit)", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    # ===============================
    # DETECT + CONTROL
    # ===============================
    if trigger_predict and target_class is not None:
        results = model_object.predict(frame, imgsz=512, conf=0.7, verbose=False)
        boxes = results[0].boxes

        matched = []
        # NOTE: found_object ตั้งค่าแบบ latch (ตามที่คุณต้องการ)
        # found_object = False  # ถ้าคุณอยากให้ค้นหาใหม่ทุกเฟรม ให้เปิดบรรทัดนี้

        if boxes is not None and len(boxes) > 0:
            for i in range(len(boxes)):
                cls_id = int(boxes.cls[i].item())
                name = model_object.names[cls_id]

                if name == target_class:
                    found_object = True

                    # หยุด search ครั้งแรกที่เจอ
                    if object_firsttime:
                        spi.send(b"s")
                        object_firsttime = False

                    x1, y1, x2, y2 = boxes.xyxy[i].cpu().numpy()
                    conf = float(boxes.conf[i].item()) if boxes.conf is not None else 0.0
                    matched.append((conf, (x1, y1, x2, y2)))

                    # distance (ของเดิม)
                    # ถ้า Width_real คือ "ความกว้างจริง" แนะนำใช้ (x2-x1)
                    width_Camera_object = (y2 - y1)
                    distance = (Width_real[name] * Focus_real) / width_Camera_object if width_Camera_object != 0 else 0.0

                    dx, dy = find_robot_middle(frame, x1, y1, x2, y2)
                    centered = (abs(dx) <= TOL)

                    # ===============================
                    # CONTROL + AUTO CALIBRATION (pulse state machine)
                    # ===============================
                    now = time.time()

                    # (A) กำลังทำ calibrate step อยู่ → ไม่ส่งคำสั่งใหม่
                    if cal_state == 1:
                        if now - cal_t1 >= cal_dt:
                            spi.send(b"s")
                            cal_state = 2
                            cal_t2 = now

                    elif cal_state == 2:
                        if now - cal_t2 >= CAL_PAUSE:
                            dx2 = dx
                            dpx = abs(dx2 - cal_dx1)

                            if cal_dt > 1e-6 and dpx >= DPX_MIN:
                                new_rate = dpx / cal_dt
                                new_rate = clamp(new_rate, RATE_MIN, RATE_MAX)

                                if cal_dir == b"r":
                                    if rate_r is None:
                                        rate_r = new_rate
                                    else:
                                        rate_r = (1 - RATE_ALPHA) * rate_r + RATE_ALPHA * new_rate
                                else:
                                    if rate_l is None:
                                        rate_l = new_rate
                                    else:
                                        rate_l = (1 - RATE_ALPHA) * rate_l + RATE_ALPHA * new_rate

                                print(
                                    f"[CAL] dir={cal_dir} dx1={cal_dx1:.1f} dx2={dx2:.1f} dpx={dpx:.1f} "
                                    f"dt={cal_dt:.3f} new={new_rate:.1f} "
                                    f"rate_r={(0 if rate_r is None else rate_r):.1f} "
                                    f"rate_l={(0 if rate_l is None else rate_l):.1f}"
                                )

                            cal_state = 0

                    # (B) idle → คุมมอเตอร์ + เริ่ม calibrate ใหม่
                    if cal_state == 0:
                        if centered:
                            spi.send(b"s")
                        else:
                            cal_dir = b"r" if dx > 0 else b"l"

                            use_rate = rate_r if cal_dir == b"r" else rate_l
                            if use_rate is not None and use_rate > 1:
                                est_dt = abs(dx) / use_rate
                                cal_dt = clamp(est_dt, MIN_DT, MAX_DT)
                            else:
                                cal_dt = 0.08  # ยังไม่รู้ rate ใช้ค่าเริ่มต้น

                            cal_dx1 = dx
                            cal_t1 = now
                            spi.send(cal_dir)
                            cal_state = 1
                    # ===============================

                    # overlay
                    cv2.putText(frame, f"dx,dy=({dx:.0f},{dy:.0f})", (10, 70),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                (0, 255, 0) if centered else (0, 0, 255), 2)

                    if centered:
                        cv2.putText(frame, "Centered!", (10, 90),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

                    # เจอ target แล้วพอ (กันสั่งหลายกล่องในเฟรมเดียว)
                    break

        # ถ้ายังไม่เคยเจอเลย → หมุนค้นหา
        if not found_object:
            spi.send(b"c")

        # draw best match (ของเดิม)
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

    # ===============================
    # SHOW
    # ===============================
    cv2.imshow("camera", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        spi.send(b"s")
        break

    if key in key_to_class:
        target_class = key_to_class[key]
        trigger_predict = True

        # reset state for a new target selection
        found_object = False
        object_firsttime = True
        cal_state = 0
        cal_dir = b"s"
        cal_dt = 0.08
        rate_r = None
        rate_l = None

cap.release()
cv2.destroyAllWindows()
try:
    spi.close()
except Exception:
    pass
