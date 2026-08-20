import os
import shutil

def extract_individual_items_fast(assets_dir, output_dir):
    """
    Sistem düzeyinde direkt dosya kopyalama yaparak
    saniyeler içinde binlerce kıyafet spritesheet'ini ayıklar.
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
                
                # Vücut, yüz, saç, kafa, gölge katmanlarını ELE
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

                # Hedef klasörü oluştur
                target_dir = os.path.join(output_dir, category)
                os.makedirs(target_dir, exist_ok=True)

                # Temiz dosya ismi oluştur
                clean_name = rel_path.replace("/", "_")
                target_path = os.path.join(target_dir, clean_name)

                # Doğrudan hızlı kopyalama (Pillow kullanmadan, saniyeler sürer)
                shutil.copy2(full_path, target_path)
                count += 1

    print(f"Toplam {count} adet bağımsız kıyafet spritesheet'i '{output_dir}' klasörüne aktarıldı!")

if __name__ == "__main__":
    extract_individual_items_fast("lpc_assets", "dist_items")
    
