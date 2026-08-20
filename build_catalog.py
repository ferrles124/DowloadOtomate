import os
import json
import random

def scan_and_generate(assets_dir):
    catalog = {
        "pants": [],
        "shirts": [],
        "shoes": []
    }
    
    if not os.path.exists(assets_dir):
        print(f"Hata: {assets_dir} bulunamadı!")
        return

    # 1. LPC Kıyafetlerini Tarama
    for root, _, files in os.walk(assets_dir):
        for file in files:
            if file.endswith(".png"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, assets_dir).replace("\\", "/")
                
                # Vücut, yüz, saç katmanlarını ELE
                if any(x in rel_path for x in ["body", "hair", "head", "face", "eyes"]):
                    continue
                
                if "legs" in rel_path or "pants" in rel_path:
                    catalog["pants"].append(rel_path)
                elif "torso" in rel_path or "shirts" in rel_path:
                    catalog["shirts"].append(rel_path)
                elif "feet" in rel_path or "shoes" in rel_path:
                    catalog["shoes"].append(rel_path)

    with open("outfits_catalog.json", "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)
    print("Katalog 'outfits_catalog.json' olarak kaydedildi.")

    # 2. Otomatik 50 Kombin Üretme (Eğer kataloğumuzda yeterli eleman varsa)
    os.makedirs("outfits", exist_ok=True)
    
    # Sadece klasör boşsa veya otomatik üretilsin isteniyorsa 50 tane üret
    existing_json = [f for f in os.listdir("outfits") if f.endswith(".json")]
    if len(existing_json) < 5:
        print("Otomatik 50 kıyafet kombini hazırlanıyor...")
        for i in range(1, 51):
            layers = []
            if catalog["pants"]:
                layers.append(random.choice(catalog["pants"]))
            if catalog["shirts"]:
                layers.append(random.choice(catalog["shirts"]))
            if catalog["shoes"]:
                layers.append(random.choice(catalog["shoes"]))

            outfit_data = {
                "outfit_name": f"outfit_casual_{i:03d}",
                "layers": layers
            }
            
            with open(f"outfits/outfit_casual_{i:03d}.json", "w", encoding="utf-8") as f:
                json.dump(outfit_data, f, indent=2)

if __name__ == "__main__":
    scan_and_generate("lpc_assets")
    
