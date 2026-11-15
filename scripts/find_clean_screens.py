import json

with open('C:/Users/User/.gemini/antigravity/brain/b6c18e6e-846f-4320-a1a4-aab0dc148d2b/.system_generated/steps/575/output.txt', 'r', encoding='utf-8') as f:
    data = json.load(f)

screens = data.get('screens', [])
print("=== Screens with REMOVE or clean or inpaint ===")
for i, s in enumerate(screens):
    title = str(s.get('title') or '')
    prompt = str(s.get('prompt') or '')
    text = (title + ' ' + prompt).lower()
    if 'remove' in text or 'inpaint' in text or 'clean seamless' in text:
        sid = s['name'].split('/')[-1]
        url = s.get('screenshot', {}).get('downloadUrl', '')
        print(f"[{i:02d}] {sid}: {title[:80]}")
        print(f"     URL: {url[:70]}...\n")
