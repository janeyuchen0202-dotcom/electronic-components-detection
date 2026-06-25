import cv2
import os
import sys
import numpy as np
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from ultralytics import YOLO

# 只顯示信心 >= 此門檻的偵測結果
CONFIDENCE_THRESHOLD = 0.4

# 以此程式所在資料夾為基準，避免工作目錄不同造成找不到檔案
HERE = os.path.dirname(os.path.abspath(__file__))

# 每個類別的框線顏色 (BGR)，讓畫面更易辨識
PALETTE = [
    (255, 56, 56), (255, 159, 56), (255, 235, 56), (153, 255, 56),
    (56, 255, 92), (56, 255, 204), (56, 204, 255), (56, 92, 255),
    (153, 56, 255), (255, 56, 235), (255, 56, 122), (180, 120, 90),
    (120, 180, 90),
]


def load_chinese_font(size=28):
    """載入可顯示中文的字型 (Windows 內建)。cv2 無法畫中文，故改用 PIL。"""
    for font_path in (
        r"C:\Windows\Fonts\msjh.ttc",
        r"C:\Windows\Fonts\mingliu.ttc",
        r"C:\Windows\Fonts\simsun.ttc",
    ):
        if os.path.exists(font_path):
            return ImageFont.truetype(font_path, size)
    return ImageFont.load_default()


def draw_detections(frame, boxes, names, font):
    """用 PIL 畫出每個偵測框與（可含中文的）類別標籤。"""
    img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)

    for box in boxes:
        conf = float(box.conf[0])
        if conf < CONFIDENCE_THRESHOLD:
            continue
        cls_id = int(box.cls[0])
        x1, y1, x2, y2 = (int(v) for v in box.xyxy[0])
        color = PALETTE[cls_id % len(PALETTE)]
        rgb = (color[2], color[1], color[0])  # BGR -> RGB
        label = f"{names[cls_id]} {conf:.0%}"

        draw.rectangle([x1, y1, x2, y2], outline=rgb, width=3)
        # 標籤底色方塊
        tb = draw.textbbox((0, 0), label, font=font)
        tw, th = tb[2] - tb[0], tb[3] - tb[1]
        ty = max(0, y1 - th - 6)
        draw.rectangle([x1, ty, x1 + tw + 8, ty + th + 6], fill=rgb)
        draw.text((x1 + 4, ty + 2), label, font=font, fill=(0, 0, 0))

    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)


def open_writer(out_dir, width, height, fps):
    """建立錄影 VideoWriter。優先用 mp4 (mp4v)，若環境不支援則退回 avi (XVID)。"""
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    for ext, codec in (('mp4', 'mp4v'), ('avi', 'XVID')):
        path = os.path.join(out_dir, f'rec_{ts}.{ext}')
        writer = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*codec), fps, (width, height))
        if writer.isOpened():
            return writer, path
        writer.release()
    return None, None


def main():
    # train.py 訓練完會把最佳權重複製到專案根目錄的 best.pt
    model_path = os.path.join(HERE, 'best.pt')

    try:
        print(f"正在載入模型: {model_path} ...")
        model = YOLO(model_path)
    except FileNotFoundError:
        print(f"[錯誤] 找不到模型檔案: {model_path}")
        print("請確認您已完成訓練 (python train.py)。")
        sys.exit(1)
    except Exception as e:
        print(f"[錯誤] 載入模型時發生問題: {e}")
        sys.exit(1)

    names = model.names
    font = load_chinese_font(28)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[錯誤] 無法開啟攝影機，請確認裝置是否正確連接，且未被其他程式佔用。")
        sys.exit(1)

    # 錄影輸出資料夾與影格率（攝影機回報的 FPS 常不可靠，無效時退回 20）
    out_dir = os.path.join(HERE, 'recordings')
    os.makedirs(out_dir, exist_ok=True)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if not fps or fps <= 1:
        fps = 20.0
    writer = None  # None 表示目前未錄影

    print("[成功] 成功開啟攝影機！開始即時物件偵測。")
    print("[提示] 點擊影像視窗後：按 'r' 開始/停止錄影，按 'q' 退出程式。")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("無法讀取攝影機畫面。")
            break

        results = model.predict(source=frame, conf=CONFIDENCE_THRESHOLD, verbose=False)
        frame = draw_detections(frame, results[0].boxes, names, font)

        # 錄影中：先寫入乾淨畫面，再於預覽畫面疊上紅色 REC 標記（不會錄進影片）
        if writer is not None:
            writer.write(frame)
            cv2.circle(frame, (26, 26), 10, (0, 0, 255), -1)
            cv2.putText(frame, "REC", (44, 34), cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (0, 0, 255), 2, cv2.LINE_AA)

        cv2.imshow("Electronic Components Detection  (R: record  Q: quit)", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("\n[提示] 接收到 'q' 鍵指令，正在關閉程式...")
            break
        elif key == ord('r'):
            if writer is None:
                h, w = frame.shape[:2]
                writer, out_path = open_writer(out_dir, w, h, fps)
                if writer is None:
                    print("[錯誤] 無法建立錄影檔（此環境缺少可用的影片編碼器）。")
                else:
                    print(f"[錄影] 開始錄影 -> {out_path}")
            else:
                writer.release()
                writer = None
                print("[錄影] 已停止並儲存。")

    if writer is not None:
        writer.release()
        print("[錄影] 已停止並儲存。")
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
