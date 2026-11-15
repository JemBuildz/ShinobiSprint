import json

with open('C:/Users/User/.gemini/antigravity/brain/b5eb2450-dfed-438f-a33e-da28992dbc17/all_stitch_screens_summary.json', 'r', encoding='utf-8') as f:
    screens = json.load(f)

for s in screens:
    t = s['title']
    if not any(t.startswith(x) for x in ['2D side-scrolling', 'Clean seamless', 'Edit this', 'Modular 2D', 'Modular wooden', 'Modular environment', '2D video game modular']):
        print(s['id'], f"[{s['w']}x{s['h']}]", t[:100])
