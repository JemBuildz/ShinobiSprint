import json

with open('C:/Users/User/.gemini/antigravity/brain/b5eb2450-dfed-438f-a33e-da28992dbc17/all_stitch_screens_summary.json', 'r', encoding='utf-8') as f:
    screens = json.load(f)

for s in screens:
    t = s['title'].lower()
    if 'sprite' in t and ('sheet' in t or 'pack' in t or 'asset' in t):
        print(s['id'], f"[{s['w']}x{s['h']}]", s['title'][:100])
