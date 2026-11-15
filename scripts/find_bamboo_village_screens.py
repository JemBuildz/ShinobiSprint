import json

with open('C:/Users/User/.gemini/antigravity/brain/b6c18e6e-846f-4320-a1a4-aab0dc148d2b/.system_generated/steps/575/output.txt', 'r', encoding='utf-8') as f:
    data = json.load(f)

screens = data.get('screens', [])
print(f"Total screens: {len(screens)}")

bamboo_screens = []
for i, s in enumerate(screens):
    title = str(s.get('title') or '')
    prompt = str(s.get('prompt') or '')
    text = (title + ' ' + prompt).lower()
    if 'bamboo' in text or 'village' in text or 'pagoda' in text or 'dojo' in text:
        sid = s['name'].split('/')[-1]
        download_url = s.get('screenshot', {}).get('downloadUrl', '')
        bamboo_screens.append({
            'index': i,
            'screen_id': sid,
            'title': title,
            'download_url': download_url
        })

print(f"Found {len(bamboo_screens)} screens matching bamboo / village:")
for b in bamboo_screens:
    print(f"[{b['index']:02d}] {b['screen_id']}")
    print(f"     Title: {b['title'][:90]}...")
    print(f"     URL: {b['download_url'][:80]}...\n")

with open('scripts/bamboo_village_screens.json', 'w', encoding='utf-8') as f:
    json.dump(bamboo_screens, f, indent=2)
