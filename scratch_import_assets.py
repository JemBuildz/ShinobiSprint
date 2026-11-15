import os
import json
import shutil
from PIL import Image

src_dir = 'C:/Users/User/.gemini/antigravity/brain/b5eb2450-dfed-438f-a33e-da28992dbc17/sliced_foes'
dest_dir = 'assets/images/foes'
os.makedirs(dest_dir, exist_ok=True)

# Mapping from sliced file name to game asset name
asset_map = {
    'ashigaru.png': 'ashigaru.png',
    'ronin.png': 'ronin.png',
    'archer.png': 'archer.png',
    'sumo.png': 'sumo.png',
    'oni.png': 'oni.png',
    'tengu.png': 'tengu.png',
    'tsuchigumo.png': 'tsuchigumo.png',
    'hitodama.png': 'hitodama.png',
    'karakasa_obake.png': 'karakasa.png',
    'ancestral_katana.png': 'ancestral_katana.png',
    'cursed_well.png': 'cursed_well.png',
    'broken_stone_lantern.png': 'broken_lantern.png',
    'ninja_blue_standing.png': 'ninja_blue.png',
    'ninja_brown_prayer.png': 'ninja_brown.png',
    'ninja_cyan_crouch.png': 'ninja_cyan.png',
    'ninja_purple_kunoichi.png': 'ninja_purple.png',
    'ninja_dark_infiltrator.png': 'ninja_dark.png',
    'ninja_ghostly.png': 'ninja_ghostly.png',
    'kitsune_trio.png': 'kitsune.png',
    'shadow_portal.png': 'shadow_portal.png',
    'oni_rage_ofuda.png': 'ofuda_talisman.png',
    'tengu_gust.png': 'tengu_gust.png',
    'smoke_cloud.png': 'smoke_puff.png',
    'cursed_arrow.png': 'cursed_arrow.png',
    'magatama_cluster.png': 'magatama.png',
    'caltrops_cluster.png': 'caltrops.png'
}

manifest = {}

for src_name, dest_name in asset_map.items():
    s_path = os.path.join(src_dir, src_name)
    d_path = os.path.join(dest_dir, dest_name)
    if os.path.exists(s_path):
        shutil.copyfile(s_path, d_path)
        im = Image.open(d_path)
        manifest[dest_name] = {
            'width': im.width,
            'height': im.height,
            'asset_path': f'foes/{dest_name}'
        }
        print(f'Imported {dest_name}: {im.size}')

# Write manifest JSON for data-driven game usage
manifest_path = os.path.join(dest_dir, 'foes_manifest.json')
with open(manifest_path, 'w', encoding='utf-8') as f:
    json.dump(manifest, f, indent=2)

print(f'Exported manifest to {manifest_path} with {len(manifest)} entries!')
