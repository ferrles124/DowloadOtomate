import os
import shutil

def extract_normal_male_outfits(assets_dir, output_dir):
    """
    LPC deposundan sadece erkek karaktere uygun,
    normal/usturuplu günlük kıyafetleri seçer ve 'normal_male' klasörüne toplar.
    """
    if not os.path.exists(assets_dir):
        print(f"Hata: {assets_dir} klasörü bulunamadı!")
        return

    # Sadece erkek ve nötr kıyafet yolları / anahtar kelimeleri
    valid_categories = {
        "shirts": ["shirts", "jackets", "vests"],
        "pants": ["pants"],
        "shoes": ["shoes", "boots"]
    }

    # Elenecek kelimeler (Fantezi, kadın, zırh, ork vb.)
    exclude_keywords = [
        "female", "dress", "skirt", "bikini", "robe", 
        "armor", "chainmail", "plate", "plate_mail", 
        "skeleton", "orc", "zombie", "monster", "wizard", 
        "crown", "wings", "cape"
    ]

    count = 0
    for root, _, files in os.walk(assets_dir):
        for file in files:
            if file.endswith(".png"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, assets_dir).replace("\\", "/").lower()

                # 1. Vücut, yüz, saç ve istenmeyen fantezi/kadın kıyafetlerini ele
                if any(x in rel_path for x in ["body", "hair", "head", "face", "eyes", "shadow"] + exclude_keywords):
                    continue

                # 2. Sadece erkek veya ortak kullanım (male/unisex) kıyafetleri al
                if "female" in rel_path:
                    continue

                # 3. Kategori belirle
                category = None
                if any(p in rel_path for p in valid_categories["pants"]):
                    category = "pants"
                elif any(s in rel_path for s in valid_categories["shirts"]):
                    category = "shirts"
                elif any(sh in rel_path for sh in valid_categories["shoes"]):
                    category = "shoes"

                if not category:
                    continue

                # Target klasör: dist_items/normal_male/shirts vb.
                target_dir = os.path.join(output_dir, "normal_male", category)
                os.makedirs(target_dir, exist_ok=True)

                clean_name = rel_path.replace("/", "_")
                target_path = os.path.join(target_dir, clean_name)

                shutil.copy2(full_path, target_path)
                count += 1

    print(f"Toplam {count} adet normal erkek kıyafeti 'dist_items/normal_male/' klasörüne ayrıştırıldı!")

if __name__ == "__main__":
    extract_normal_male_outfits("lpc_assets", "dist_items")
    
