import os
import json
from PIL import Image

def extract_individual_items(assets_dir, output_dir):
    """
    LPC deposundaki tüm giysileri tek tek bulur,
    vücut/yüz/saç öğelerini eler ve her bir giysiyi 
    kendi kategorisinde tek başına şeffaf PNG olarak kaydeder.
    """
    if not os.path.exists(assets_dir):
        print(f"Hata: {assets_dir} klasörü bulunamadı!")
        return

    count = 0
    for root, _, files in os.walk(assets_dir):
        for file in files:
            if file.endswith(".png"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, assets_dir).replace("\\", "/")
                
                # Vücut, yüz, saç, kafa katmanlarını ELE
                if any(x in rel_path for x in ["body", "hair", "head", "face", "eyes", "shadow"]):
                    continue
                
                # Kategoriyi belirle
                category = "others"
                if "legs" in rel_path or "pants" in rel_path:
                    category = "pants"
                elif "torso" in rel_path or "shirts" in rel_path or "jackets" in rel_path:
                    category = "shirts"
                elif "feet" in rel_path or "shoes" in rel_path or "boots" in rel_path:
                    category = "shoes"
                elif "weapons" in rel_path or "shield" in rel_path:
                    category = "weapons"

                # Hedef kaydetme klasörünü oluştur (Örn: dist_items/pants/)
                target_dir = os.path.join(output_dir, category)
                os.makedirs(target_dir, exist_ok=True)

                # Temiz dosya ismi oluştur (Örn: legs_pants_male_blue.png)
                clean_name = rel_path.replace("/", "_")
                target_path = os.path.join(target_dir, clean_name)

                # Görseli açıp direkt şeffaf olarak kaydet
                try:
                    img = Image.open(full_path).convert("RGBA")
                    img.save(target_path, "PNG")
                    count += 1
                except Exception as e:
                    print(f"Hata ({rel_path}): {e}")

    print(f"Toplam {count} adet bağımsız kıyafet/öğe üretildi ve '{output_dir}' klasörüne kaydedildi!")

if __name__ == "__main__":
    extract_individual_items("lpc_assets", "dist_items")
                    
