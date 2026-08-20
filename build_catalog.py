import os
import json

def scan_lpc_items(assets_dir):
    catalog = {
        "pants": [],
        "shirts": [],
        "shoes": []
    }
    
    if not os.path.exists(assets_dir):
        print(f"Hata: {assets_dir} klasörü bulunamadı!")
        return

    for root, _, files in os.walk(assets_dir):
        for file in files:
            if file.endswith(".png"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, assets_dir).replace("\\", "/")
                
                # Vücut, saç, kafa katmanlarını tamamen dışla
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
    print("Katalog başarıyla 'outfits_catalog.json' olarak kaydedildi!")

if __name__ == "__main__":
    scan_lpc_items("lpc_assets")
  
