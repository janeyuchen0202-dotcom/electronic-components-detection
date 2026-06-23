import os
import sys
from PIL import Image
from pillow_heif import register_heif_opener

# 修正 Windows 中文環境 (cp950) 無法輸出 emoji 的問題
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# 註冊 HEIC 開啟器，讓 Pillow 能夠支援 .HEIC 格式讀取
register_heif_opener()

# 設定資料夾路徑
BASE_DIR = "影像辨識資料集"
OUTPUT_DIR = "dataset_images" # 建立一個新資料夾來存放轉換後與重新命名的圖片

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # 取得基礎資料夾下的所有類別目錄
    categories = [d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d))]

    for category in categories:
        category_path = os.path.join(BASE_DIR, category)
        output_category_path = os.path.join(OUTPUT_DIR, category)
        
        if not os.path.exists(output_category_path):
            os.makedirs(output_category_path)
            
        # 篩選出圖片檔案
        images = [f for f in os.listdir(category_path) if f.lower().endswith(('.heic', '.jpg', '.jpeg', '.png'))]
        
        for idx, img_name in enumerate(images):
            img_path = os.path.join(category_path, img_name)
            # 新檔名格式：類別名稱_編號.jpg (四位數補零)
            new_name = f"{category}_{idx+1:04d}.jpg"
            new_path = os.path.join(output_category_path, new_name)
            
            try:
                # 讀取圖片，並轉換為 RGB 模式以儲存為標準 JPG
                image = Image.open(img_path)
                image = image.convert('RGB')
                image.save(new_path, "JPEG", quality=95)
                print(f"✅ 已處理: {img_path} -> {new_path}")
            except Exception as e:
                print(f"❌ 處理圖片 {img_name} 時發生錯誤: {e}")

    print("\n🎉 批次重新命名與格式轉換完成！請至 dataset_images 目錄查看。")

if __name__ == '__main__':
    main()
