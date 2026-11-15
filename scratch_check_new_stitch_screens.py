import json

with open('C:/Users/User/.gemini/antigravity/brain/b5eb2450-dfed-438f-a33e-da28992dbc17/.system_generated/steps/3286/output.txt', 'r', encoding='utf-8') as f:
    data = json.load(f)

screens = data.get('screens', [])
print(f'Total screens now in Shinobi Sprint: {len(screens)}')

# Load old summary to find newly added screens
try:
    with open('C:/Users/User/.gemini/antigravity/brain/b5eb2450-dfed-438f-a33e-da28992dbc17/all_stitch_screens_summary.json', 'r', encoding='utf-8') as f:
        old_screens = json.load(f)
    old_ids = set(s['id'] for s in old_screens)
except Exception as e:
    old_ids = set()

print(f'Previous screen count was: {len(old_ids)}')

new_screens = []
for s in screens:
    name = s.get('name', '')
    sid = name.split('/')[-1]
    title = s.get('title', '')
    screenshot = s.get('screenshot', {})
    url = screenshot.get('downloadUrl', '')
    w = s.get('width', '')
    h = s.get('height', '')
    create_time = s.get('createTime', '')
    update_time = s.get('updateTime', '')
    
    if sid not in old_ids:
        new_screens.append({
            'id': sid,
            'title': title,
            'url': url,
            'w': w,
            'h': h,
            'name': name
        })

print(f'Found {len(new_screens)} brand new screens!')
for ns in new_screens:
    print('='*60)
    print(f"ID: {ns['id']} [{ns['w']}x{ns['h']}]")
    print(f"Title: {ns['title']}")
    print(f"URL: {ns['url']}")

with open('C:/Users/User/.gemini/antigravity/brain/b5eb2450-dfed-438f-a33e-da28992dbc17/new_stitch_screens.json', 'w', encoding='utf-8') as f_out:
    json.dump(new_screens, f_out, indent=2)
