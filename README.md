# 電子元件即時物件偵測系統 (Electronic Components Object Detection)

這是一個基於 **YOLOv8** 開發的輕量級物件偵測專案。目標是透過攝影機**即時偵測並框出**學校實驗室常見的 13 種電子元件（二極體、三用電表、麵包版等），在畫面上以方框標示位置，並以中文顯示類別與信心程度。

## 🎯 專案目標

- 建立一個可在一般 PC（CPU）即時運作的輕量化電子元件偵測模型。
- 自行收集照片、轉檔、標註邊界框，訓練專屬的 YOLOv8 偵測器。
- 提供完整工作流：前處理 → 標註 → 建立資料集 → 訓練 → 攝影機即時偵測。

## 🛠 偵測類別 (13 Classes)

`二極體`、`三用電表`、`工具箱`、`白色LED`、`紅色LED`、`測試線`、`電阻`、`電容`、`電線`、`綠色LED`、`撥線鉗`、`麵包版`、`IC`

---

## 📦 環境安裝

### ✅ 一鍵安裝執行 `run.bat`（Windows）

雙擊 **`run.bat`**，自動建立虛擬環境、安裝套件並顯示選單。

> 需先安裝 Python 3.8 ~ 3.11（安裝時勾選「Add Python to PATH」）。

### 🔧 手動安裝

```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

> **注意**：`requirements.txt` 已將 `torch` 鎖定在 `2.5.1+cpu`。較新的 torch（如 2.12.x）在部分 Windows 環境會出現 `WinError 1114（c10.dll 初始化失敗）`。

---

## 🚀 完整工作流程

```bash
# 1. 影像前處理：HEIC/JPG 統一轉成標準 JPG
python preprocess_and_rename.py

# 2. 邊界框標註：用 LabelImg 對 dataset_images 內各類圖片框出元件
#    （雙擊 label_tool.bat 啟動；左側格式請切成 YOLO）
label_tool.bat

# 3. 建立偵測資料集：整理標註、切分 train/val、產生 data.yaml
python build_dataset_det.py

# 4. 訓練 YOLOv8 偵測模型（完成後自動產生 best.pt）
python train.py

# 5. 攝影機即時偵測（畫面內按 q 離開）
python detect.py
```

---

## 📁 主要檔案說明

| 檔案 | 功能 |
|------|------|
| `preprocess_and_rename.py` | 將原始照片（含 HEIC）轉成標準 JPG，輸出至 `dataset_images` |
| `label_tool.bat` | 啟動 LabelImg 進行邊界框標註（YOLO 格式） |
| `build_dataset_det.py` | 整理標註、切分 train/val、建立 `dataset_det/` 與 `data.yaml` |
| `train.py` | 載入 YOLOv8n 訓練偵測模型，完成後複製最佳權重為 `best.pt` |
| `detect.py` | 開啟攝影機即時偵測，畫出彩色方框與中文類別 / 信心值，按 `q` 離開 |
| `data.yaml` | 偵測資料集設定（類別、路徑），由 `build_dataset_det.py` 自動產生 |

---

## 📜 授權與開源參考

- 核心演算法基於 [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)（**AGPL-3.0**）。
- 標註工具 [LabelImg](https://github.com/HumanSignal/labelImg)（MIT）。
- HEIC 讀取 [pillow-heif](https://github.com/bigcat88/pillow_heif)；影像處理 [OpenCV](https://opencv.org/)；框架 [PyTorch](https://pytorch.org/)。
