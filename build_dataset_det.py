# -*- coding: utf-8 -*-
"""
救援並建立『物件偵測』資料集。
labelImg 先前把所有 .txt 誤存到 影像辨識資料集/二極體/，
本程式依『圖片所在資料夾 = 正確類別』為基準，修正類別編號並重建為 YOLO 偵測格式。
"""
import os, sys, shutil, random

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HERE      = os.path.dirname(os.path.abspath(__file__))
LABEL_DIR = os.path.join(HERE, "影像辨識資料集", "二極體")   # labelImg 誤存標註的位置
IMG_ROOT  = os.path.join(HERE, "dataset_images")            # 圖片（依類別分資料夾）
OUT       = os.path.join(HERE, "dataset_det")               # 輸出的偵測資料集
VAL_RATIO = 0.2
SEED      = 42

CLASSES = ["二極體","三用電表","工具箱","白色LED","紅色LED","測試線",
           "電阻","電容","電線","綠色LED","撥線鉗","麵包版","IC"]
NAME2ID = {n: i for i, n in enumerate(CLASSES)}


def main():
    random.seed(SEED)
    for sub in ("images/train","images/val","labels/train","labels/val"):
        os.makedirs(os.path.join(OUT, sub.replace('/', os.sep)), exist_ok=True)

    total_train = total_val = corrected = 0

    for cls in CLASSES:
        cls_dir = os.path.join(IMG_ROOT, cls)
        if not os.path.isdir(cls_dir):
            print(f"[略過] 找不到圖片資料夾: {cls}")
            continue
        imgs = [f for f in os.listdir(cls_dir) if f.lower().endswith('.jpg')]
        # 只取有對應標註的圖片
        paired = []
        for img in imgs:
            stem = os.path.splitext(img)[0]
            lbl = os.path.join(LABEL_DIR, stem + '.txt')
            if os.path.exists(lbl):
                paired.append((img, lbl))

        if not paired:
            print(f"[略過] {cls}: 沒有對應標註")
            continue

        random.shuffle(paired)
        n_val = max(1, int(len(paired) * VAL_RATIO))
        splits = [('val', paired[:n_val]), ('train', paired[n_val:])]

        for split, items in splits:
            for img, lbl in items:
                stem = os.path.splitext(img)[0]
                # 複製圖片
                shutil.copy2(os.path.join(cls_dir, img),
                             os.path.join(OUT, 'images', split, img))
                # 讀標註，強制類別 = 資料夾類別（修正誤標）
                cid = NAME2ID[cls]
                out_lines = []
                with open(lbl, encoding='utf-8') as fh:
                    for ln in fh:
                        parts = ln.split()
                        if len(parts) != 5:
                            continue
                        if int(parts[0]) != cid:
                            corrected += 1
                        out_lines.append(f"{cid} {parts[1]} {parts[2]} {parts[3]} {parts[4]}")
                with open(os.path.join(OUT, 'labels', split, stem + '.txt'),
                          'w', encoding='utf-8') as fo:
                    fo.write("\n".join(out_lines) + "\n")

            if split == 'train': total_train += len(items)
            else:                total_val   += len(items)

        print(f"[OK] {cls}: {len(paired)-n_val} 訓練 / {n_val} 驗證")

    # 寫出 data.yaml（用絕對路徑避免相對路徑問題）
    yaml_path = os.path.join(HERE, "data.yaml")
    with open(yaml_path, 'w', encoding='utf-8') as f:
        f.write("# YOLOv8 物件偵測資料集設定（由 build_dataset_det.py 自動產生）\n")
        f.write(f"path: {OUT}\n")
        f.write("train: images/train\n")
        f.write("val: images/val\n\n")
        f.write(f"nc: {len(CLASSES)}\n")
        f.write("names:\n")
        for i, n in enumerate(CLASSES):
            f.write(f"  {i}: {n}\n")

    print()
    print("=" * 45)
    print(f"  完成！訓練 {total_train} 張 / 驗證 {total_val} 張")
    print(f"  自動修正誤標類別: {corrected} 個")
    print(f"  偵測資料集: {OUT}")
    print(f"  設定檔: {yaml_path}")
    print("=" * 45)
    print("接下來執行：python train.py")


if __name__ == '__main__':
    main()
