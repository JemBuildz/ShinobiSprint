import json
import os
import urllib.request
from PIL import Image

os.makedirs('assets/autumn_maple', exist_ok=True)

with open('C:/Users/User/.gemini/antigravity/brain/b6c18e6e-846f-4320-a1a4-aab0dc148d2b/.system_generated/steps/575/output.txt', 'r', encoding='utf-8') as f:
    data = json.load(f)

screens = data.get('screens', [])

targets = {
    'b4483133ae8b498fafd94713224e01d1': 'autumn_bg_clean_night.png',
    'a513afd3b76045cfb8237704f0cc290d': 'autumn_panoramic_clean_night.png',
    'f3a857dde17e49bbbfec386d314d635a': 'autumn_panoramic_day.png',
    'e848767a23dd4e25ab0bdd4b85f6493a': 'autumn_bridge_lanterns_pack1.png',
    'e9d6cb4885054923bdaa75a2418a829b': 'autumn_bridge_lanterns_pack2.png',
    'e55448f4ec0a4fb7aa2b62c88014e178': 'autumn_ground_terrain_pack1.png',
    '350afbb576ef4f6bb17a5bf6cd8bcf76': 'autumn_ground_terrain_pack2.png',
    '9a0751a9cfcf448a97361be8058a118a': 'autumn_flora_maple_trees_pack1.png',
    '51ac0f7952294edd8ddde9bc137b4d90': 'autumn_flora_maple_trees_pack2.png',
    '74493a9eda8e4221a7362528cae4949e': 'autumn_props_shrines_pack.png',
    '09faf2b0c21f43358a42b6e84a63fea4': 'autumn_kitsune_statues_pack.png',
}

headers = {'User-Agent': 'Mozilla/5.0'}

for s in screens:
    sid = s['name'].split('/')[-1]
    if sid in targets:
        filename = targets[sid]
        out_path = os.path.join('assets/autumn_maple', filename)
        screenshot = s.get('screenshot') or {}
        url = screenshot.get('downloadUrl')
        if url:
            # Append =s0 for maximum native resolution
            hi_res_url = url + '=s0'
            print(f"Downloading high-res {filename} from {sid}...")
            try:
                req = urllib.request.Request(hi_res_url, headers=headers)
                with urllib.request.urlopen(req) as resp, open(out_path, 'wb') as out_f:
                    out_f.write(resp.read())
                im = Image.open(out_path)
                print(f"  -> Saved {out_path} ({os.path.getsize(out_path)} bytes, {im.size})")
            except Exception as e:
                print(f"  -> Failed to download: {e}")

print("\nAll downloaded files:")
for f in sorted(os.listdir('assets/autumn_maple')):
    p = os.path.join('assets/autumn_maple', f)
    im = Image.open(p)
    print(f"  {f:36s}: {os.path.getsize(p):7d} bytes | {im.size}")
