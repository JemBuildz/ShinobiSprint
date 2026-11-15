import json

with open('C:/Users/User/.gemini/antigravity/brain/b5eb2450-dfed-438f-a33e-da28992dbc17/all_stitch_screens_summary.json', 'r', encoding='utf-8') as f:
    screens = json.load(f)

specific_keywords = ['enemy', 'foe', 'boss', 'oni', 'ronin', 'samurai', 'monster', 'villain', 'creature', 'beast', 'demon', 'warrior', 'character sprite', 'sprite sheet of', 'isolated character']

results = []
for s in screens:
    t = s['title'].lower()
    for k in specific_keywords:
        if k in t:
            results.append((k, s))
            break

print(f'Total matches: {len(results)}')
for k, s in results:
    print(f"[{k}] ID: {s['id']} ({s['w']}x{s['h']})")
    print(f"Title: {s['title']}")
    print(f"URL: {s['url']}")
    print('-'*50)

with open('C:/Users/User/.gemini/antigravity/brain/b5eb2450-dfed-438f-a33e-da28992dbc17/character_enemy_screens.json', 'w', encoding='utf-8') as f_out:
    json.dump([s for k, s in results], f_out, indent=2)
