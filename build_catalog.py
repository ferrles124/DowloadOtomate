import os
import shutil

def filter_normal_male_items():
    """
    Dışarıya istek atmadan, repodaki mevcut klasörleri tarar
    ve sadece normal/usturuplu erkek kıyafetlerini 'dist_items/normal_male/' klasörüne süzer.
    """
    # Önceden indirilmiş olan yerel klasör yolları
    possible_source_dirs = ["lpc_assets", "dist_items"]
    
    source_dir = None
    for d in possible_source_dirs:
        if os.path.exists(d):
            source_dir = d
            break

    if not source_dir:
        print("Hata: Repoda taranacak yerel görsel klasörü bulunamadı!")
        return

    # Süzülecek kategoriler
    valid_categories = {
        "shirts": ["shirts", "jackets", "vests"],
        "pants": ["pants"],
        "shoes": ["shoes", "boots"]
    }

    # Elenecek kadın/fantezi/zırh kelimeleri
    exclude_keywords = [
        "female", "dress", "skirt", "bikini", "robe", 
        "armor", "chainmail", "plate", "plate_mail", 
        "skeleton", "orc", "zombie", "monster", "wizard", 
        "crown", "wings", "cape"
    ]

    count = 0
    for root, _, files in os.walk(source_dir):
        # Zaten oluşmuş olan normal_male klasörünü tekrar taramamak için atla
        if "normal_male" in root:
            continue

        for file in files:
            if file.endswith(".png"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, source_dir).replace("\\", "/").lower()

                # 1. Vücut, yüz, saç ve fantezi/kadın kıyafetlerini ele
                if any(x in rel_path for x in ["body", "hair", "head", "face", "eyes", "shadow"] + exclude_keywords):
                    continue

                # 2. Sadece erkek veya ortak (unisex) olanları al
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

                # Hedef dizin: dist_items/normal_male/<kategori>/
                target_dir = os.path.join("dist_items", "normal_male", category)
                os.makedirs(target_dir, exist_ok=True)

                clean_name = rel_path.replace("/", "_")
                target_path = os.path.join(target_dir, clean_name)

                shutil.copy2(full_path, target_path)
                count += 1

    print(f"İşlem Tamamlandı! Toplam {count} adet normal erkek kıyafeti yerel olarak 'dist_items/normal_male/' klasörüne süzüldü.")

if __name__ == "__main__":
    filter_normal_male_items()
    
