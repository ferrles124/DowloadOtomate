import json
import os
from PIL import Image

def generate_outfit(config_path, assets_dir, output_dir):
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                print(f"Uyarı: Boş dosya atlanıyor -> {config_path}")
                return
            config = json.loads(content)
    except json.JSONDecodeError:
        print(f"Hata: Geçersiz/Bozuk JSON dosyası atlanıyor -> {config_path}")
        return
    except Exception as e:
        print(f"Hata oluştu ({config_path}): {e}")
        return

    outfit_image = None

    for layer_path in config.get('layers', []):
        full_path = os.path.join(assets_dir, layer_path)
        if os.path.exists(full_path):
            layer_img = Image.open(full_path).convert("RGBA")
            if outfit_image is None:
                outfit_image = Image.new("RGBA", layer_img.size, (0, 0, 0, 0))
            
            outfit_image.alpha_composite(layer_img)
        else:
            print(f"Uyarı: Katman bulunamadı -> {layer_path}")

    if outfit_image:
        os.makedirs(output_dir, exist_ok=True)
        out_name = config.get('outfit_name', os.path.splitext(os.path.basename(config_path))[0])
        out_path = os.path.join(output_dir, f"{out_name}.png")
        outfit_image.save(out_path, "PNG")
        print(f"Başarıyla üretildi: {out_path}")

if __name__ == "__main__":
    configs_dir = "outfits"
    if os.path.exists(configs_dir):
        for file in os.listdir(configs_dir):
            if file.endswith(".json"):
                generate_outfit(os.path.join(configs_dir, file), "lpc_assets", "dist_outfits")
                
