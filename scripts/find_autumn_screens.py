import json

with open('C:/Users/User/.gemini/antigravity/brain/b6c18e6e-846f-4320-a1a4-aab0dc148d2b/.system_generated/steps/575/output.txt', 'r', encoding='utf-8') as f:
    data = json.load(f)

screens = data.get('screens', [])
print(f'Total screens in project: {len(screens)}')
print('=== Screens matching Autumn / Maple ===')

results = []
for i, s in enumerate(screens):
    title = str(s.get('title') or '')
    prompt = str(s.get('prompt') or '')
    combined = (title + ' ' + prompt).lower()
    if 'autumn' in combined or 'maple' in combined:
        screen_id = s.get('name', '').split('/')[-1]
        fe = s.get('fileEntries', [])
        entries = []
        for entry in fe:
            name = entry.get('name', '')
            url = entry.get('downloadUrl', '')
            entries.append({'name': name, 'url': url})
        results.append({
            'index': i,
            'screen_id': screen_id,
            'title': title,
            'prompt': prompt,
            'entries': entries
        })

print(f'Found {len(results)} matching screens:')
for r in results:
    print(f"\n[{r['index']:02d}] ScreenID: {r['screen_id']}")
    print(f"     Title: {r['title']}")
    print(f"     Prompt: {r['prompt'][:120]}...")
    for e in r['entries']:
        print(f"     FileEntry: {e['name']} -> {e['url'][:90]}...")

with open('scripts/autumn_screens.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)
