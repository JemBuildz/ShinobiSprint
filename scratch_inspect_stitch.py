import json

with open('C:/Users/User/.gemini/antigravity/brain/b5eb2450-dfed-438f-a33e-da28992dbc17/.system_generated/steps/3222/output.txt', 'r', encoding='utf-8') as f:
    data = json.load(f)

screens = data.get('screens', [])
print(f'Total screens: {len(screens)}')

results = []
for i, s in enumerate(screens):
    title = s.get('title', '')
    name = s.get('name', '')
    screenshot = s.get('screenshot', {})
    url = screenshot.get('downloadUrl', '')
    w = s.get('width', '')
    h = s.get('height', '')
    results.append({'idx': i, 'id': name.split('/')[-1], 'title': title, 'url': url, 'w': w, 'h': h})

keywords = ['enemy', 'character', 'foe', 'boss', 'oni', 'samurai', 'ronin', 'sprite', 'monster', 'villain', 'creature', 'beast', 'demon', 'warrior', 'ninja', 'archer']

print('\n=== KEYWORD MATCHES ===')
matches = []
for r in results:
    t = r['title'].lower()
    matched = [k for k in keywords if k in t]
    if matched:
        matches.append((r, matched))
        print(f"[{r['idx']}] ID: {r['id']} ({r['w']}x{r['h']}) Matched: {matched}")
        print(f"     Title: {r['title'][:140]}...")
        print(f"     URL: {r['url'][:90]}...")

print(f'\nTotal keyword matches: {len(matches)}')

# Also print all screens that are NOT 16:9 backgrounds (e.g. not width 1024 / height 576 or 1024x768 etc.)
print('\n=== ALL NON-STANDARD SIZES OR UNIQUE TITLES ===')
with open('C:/Users/User/.gemini/antigravity/brain/b5eb2450-dfed-438f-a33e-da28992dbc17/all_stitch_screens_summary.json', 'w', encoding='utf-8') as out:
    json.dump(results, out, indent=2)
print('Wrote all_stitch_screens_summary.json')
