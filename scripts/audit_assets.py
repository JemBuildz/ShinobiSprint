import os
import re

asset_pattern = re.compile(r"['\"]([a-zA-Z0-9_\-/\.]+\.(png|jpg|mp3|wav|tmx|tsx))['\"]")
referenced = set()

for root, dirs, files in os.walk('lib'):
    for f in files:
        if f.endswith('.dart'):
            with open(os.path.join(root, f), 'r', encoding='utf-8', errors='ignore') as fp:
                for match in asset_pattern.findall(fp.read()):
                    referenced.add(match[0])

print(f"Total referenced asset filenames in lib: {len(referenced)}")
missing = []
found = []

for ref in sorted(referenced):
    candidates = [
        ref,
        os.path.join('assets', ref),
        os.path.join('assets/images', ref),
        os.path.join('assets/map', ref),
        os.path.join('assets/sfx', ref),
        os.path.join('assets/music', ref),
    ]
    if any(os.path.exists(c) for c in candidates):
        found.append(ref)
    else:
        missing.append(ref)

print(f"Found on disk: {len(found)}")
if missing:
    print(f"Missing assets ({len(missing)}):")
    for m in missing:
        print("  - ", m)
else:
    print("ALL code-referenced assets exist on disk!")
