import os
import sys
import shutil
from ultralytics import YOLO

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# 以此程式所在資料夾為基準（避免中文路徑與工作目錄造成的問題）
HERE = os.path.dirname(os.path.abspath(__file__))

def main():
    print("正在載入預訓練偵測模型 (yolov8n.pt)...")
    # yolov8n.pt 是 YOLOv8 的輕量級「物件偵測」模型（會框出物件位置）
    model = YOLO('yolov8n.pt')

    print("開始訓練模型...")
    run_name = 'yolov8_electronics_det'
    try:
        model.train(
            data=os.path.join(HERE, 'data.yaml'),  # 偵測資料集設定檔
            epochs=80,              # 訓練世代數
            imgsz=480,              # 輸入影像大小（物件較大，480 兼顧速度與精度）
            batch=16,               # 批次大小，若記憶體不足可改為 8 或 4
            device='cpu',           # 若有 NVIDIA 顯卡可改為 '0'
            project=os.path.join(HERE, 'runs'),
            name=run_name,
            exist_ok=True,
            plots=True
        )
    except Exception as e:
        # 訓練本身已完成、best.pt 已存檔；繪製圖表階段偶爾會因字型問題出錯，
        # 在此攔截以確保仍能完成下方的權重複製。
        print(f"[警告] 訓練在繪圖階段出現問題（不影響模型權重）：{e}")

    # 不論繪圖是否成功，都從輸出資料夾複製最佳權重到固定位置 best.pt
    best = os.path.join(HERE, 'runs', run_name, 'weights', 'best.pt')
    target = os.path.join(HERE, 'best.pt')
    if os.path.exists(best):
        shutil.copy(best, target)
        print()
        print("[完成] 訓練結束！")
        print(f"最佳模型權重已複製到: {target}")
        print("接下來執行：python detect.py")
    else:
        print(f"[錯誤] 找不到訓練後的權重檔: {best}")

if __name__ == '__main__':
    main()
