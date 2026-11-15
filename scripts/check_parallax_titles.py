import json

with open('C:/Users/User/.gemini/antigravity/brain/b6c18e6e-846f-4320-a1a4-aab0dc148d2b/.system_generated/steps/575/output.txt', 'r', encoding='utf-8') as f:
    data = json.load(f)

screens = data.get('screens', [])
indices = [4, 8, 9, 16, 18, 19, 20, 21, 23, 31, 68, 79]

for i in indices:
    if i < len(screens):
        s = screens[i]
        sid = s['name'].split('/')[-1]
        print(f"[{i:02d}] {sid}:")
        print(f"     Title: {s.get('title')}\n")
