import os
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
brain_dir = r'C:\Users\User\.gemini\antigravity\brain'

for root, dirs, files in os.walk(brain_dir):
    for f in files:
        if f == 'transcript.jsonl':
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
                    for line_no, line in enumerate(fp, 1):
                        if 'invoke_subagent' in line:
                            data = json.loads(line)
                            for c in data.get('tool_calls', []):
                                if c.get('name') == 'invoke_subagent':
                                    subs = c.get('args', {}).get('Subagents', [])
                                    for sub in subs:
                                        print(f"{path}:{line_no} Role: {sub.get('Role')} Prompt: {str(sub.get('Prompt'))[:100]}")
            except Exception as e:
                pass
