import os
import sys
import shutil
import random

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ── 設定 ──────────────────────────────────────────────
SOURCE_DIR  = "dataset_images"   # preprocess_and_rename.py 輸出的資料夾
OUTPUT_DIR  = "dataset"          # 訓練用資料集根目錄
VAL_RATIO   = 0.2                # 20% 當驗證集
RANDOM_SEED = 42
# ──────────────────────────────────────────────────────

IMAGE_EXTS = {'.jpg', '.jpeg', '.png'}

def build():
    random.seed(RANDOM_SEED)

    if not os.path.exists(SOURCE_DIR):
        print(f"[錯誤] 找不到來源資料夾: {SOURCE_DIR}")
        print("請先執行 preprocess_and_rename.py")
        sys.exit(1)

    categories = [
        d for d in os.listdir(SOURCE_DIR)
        if os.path.isdir(os.path.join(SOURCE_DIR, d))
    ]

    if not categories:
        print(f"[錯誤] {SOURCE_DIR} 裡沒有任何類別資料夾。")
        sys.exit(1)

    total_train = total_val = 0

    for category in sorted(categories):
        cat_path = os.path.join(SOURCE_DIR, category)
        images = [
            f for f in os.listdir(cat_path)
            if os.path.splitext(f)[1].lower() in IMAGE_EXTS
        ]

        if not images:
            print(f"[略過] {category}: 資料夾內沒有圖片")
            continue

        random.shuffle(images)
        val_count   = max(1, int(len(images) * VAL_RATIO))
        val_files   = images[:val_count]
        train_files = images[val_count:]

        for split, files in (('train', train_files), ('val', val_files)):
            dst_dir = os.path.join(OUTPUT_DIR, split, category)
            os.makedirs(dst_dir, exist_ok=True)
            for img_name in files:
                shutil.copy2(os.path.join(cat_path, img_name),
                             os.path.join(dst_dir, img_name))

        print(f"[OK] {category}: {len(train_files)} 訓練 / {len(val_files)} 驗證")
        total_train += len(train_files)
        total_val   += len(val_files)

    print()
    print("=" * 45)
    print(f"  完成！訓練集: {total_train} 張，驗證集: {total_val} 張")
    print(f"  資料集已建立於: {OUTPUT_DIR}/")
    print("=" * 45)
    print()
    print("接下來執行：python train.py")

if __name__ == '__main__':
    build()
