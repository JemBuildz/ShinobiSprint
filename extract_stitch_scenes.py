import json
import urllib.request
import os

with open('C:/Users/User/.gemini/antigravity/brain/b5eb2450-dfed-438f-a33e-da28992dbc17/.system_generated/steps/2766/output.txt', 'r', encoding='utf-8') as f:
    data = json.load(f)

screens = data.get('screens', [])
out_dir = 'C:/Users/User/.gemini/antigravity/brain/b5eb2450-dfed-438f-a33e-da28992dbc17/stitch_scenes'
os.makedirs(out_dir, exist_ok=True)

catalog = []

keywords = [
    ('Nighttime Sakura Village', 'sakura', 'nighttime'),
    ('Nighttime Castle Fortress', 'castle', 'nighttime'),
    ('Daytime Castle Fortress', 'castle', 'daytime'),
    ('Nighttime Waterfall Gorge', 'waterfall', 'nighttime'),
    ('Nighttime Torii Shrine Path', 'torii', 'nighttime'),
    ('Daytime Torii Shrine Path', 'torii', 'daytime'),
    ('Daytime Autumn Maple', 'maple', 'daytime'),
    ('Nighttime Autumn Maple', 'maple', 'nighttime'),
    ('Sunset Bamboo Forest', 'bamboo', 'sunset')
]

for s in screens:
    title = s.get('title', '')
    tl = title.lower()
    screenshot = s.get('screenshot', {})
    url = screenshot.get('downloadUrl', '')
    sid = s.get('name', '').split('/')[-1]
    
    if not url or len(url) < 10:
        continue

    # Only look for panoramic level maps and stages
    if ('panoramic' in tl or 'stage' in tl or 'level map' in tl or 'backdrop' in tl) and ('sprite' not in tl and 'modular' not in tl and 'cutout' not in tl):
        cat = 'Feudal Scene'
        for cname, k1, k2 in keywords:
            if k1 in tl and k2 in tl:
                cat = cname
                break
        
        catalog.append({
            'id': sid,
            'category': cat,
            'title': title,
            'url': url
        })

print(f'Found {len(catalog)} full environmental scene plates in Stitch!')

saved_scenes = []
seen_cats = set()

for item in catalog:
    cat = item['category']
    if cat in seen_cats:
        continue
    seen_cats.add(cat)
    
    safe_cat = cat.replace(' ', '_').lower()
    fname = f"{item['id'][:8]}_{safe_cat}.png"
    fpath = os.path.join(out_dir, fname)
    try:
        urllib.request.urlretrieve(item['url'], fpath)
        item['local_file'] = fpath
        saved_scenes.append(item)
        print(f"Downloaded: {cat} -> {fname}")
    except Exception as e:
        print(f"Error downloading {cat}: {e}")

print(f"Total downloaded scene images: {len(saved_scenes)}")

with open('C:/Users/User/.gemini/antigravity/brain/b5eb2450-dfed-438f-a33e-da28992dbc17/stitch_scenes/manifest.json', 'w', encoding='utf-8') as f:
    json.dump(saved_scenes, f, indent=2)
