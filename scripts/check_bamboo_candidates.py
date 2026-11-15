import json

with open('C:/Users/User/.gemini/antigravity/brain/b6c18e6e-846f-4320-a1a4-aab0dc148d2b/.system_generated/steps/575/output.txt', 'r', encoding='utf-8') as f:
    data = json.load(f)

screens = data.get('screens', [])
target_ids = [
    'ab7e926a7df14be18c8d0f4d5788b611',
    'e2b97bf5bad54cf896e7bdb7577c2f5f',
    '41efecf609f0472495fc459fb5b28fcd',
    'a1b54b0295d5420383654a09f1d1fbef',
    '544fe6d48413475ea7f3b4c643f06c26',
    '8855712562474343654',
    '13471053490021172856',
]

for s in screens:
    sid = s['name'].split('/')[-1]
    if sid in target_ids:
        print(f"=== [{sid}] ===")
        print(f"Title: {s.get('title')}")
        print(f"Prompt: {s.get('prompt')}")
        print(f"URL: {s.get('screenshot', {}).get('downloadUrl')}\n")
