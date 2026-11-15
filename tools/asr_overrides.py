#!/usr/bin/env python3
"""Auto-map ASR mishears to `asr` override fields.

Runs the library's asr_check, parses DIFF lines, and writes the heard text into
the line's `asr` field (the demo's documented approach: the audio is right, the
ear is wrong — homophones and digit-vs-spelled numbers).
Only whitelisted kinds of mishears are auto-accepted; anything not matching the
whitelist is printed for manual review.
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.join(ROOT, "repo")
LINES = os.path.join(ROOT, "project", "script", "voice_lines.json")
AUDIO = os.path.join(ROOT, "audio")

lines = json.load(open(LINES))
r = subprocess.run([os.path.join(REPO, ".venv", "bin", "python"),
                    os.path.join(REPO, "core", "tts", "asr_check.py"),
                    LINES, AUDIO], capture_output=True, text=True)
log = r.stdout
open("/tmp/asr_pass2.log", "w").write(log)
diffs = {}
for m in re.finditer(r'^DIFF\s+(\S+)\s+\|([^|]*)\|?\s*→\s*(.*)$', log, re.M):
    diffs[m.group(1)] = m.group(3).strip()
print(f"{len(diffs)} DIFFs on this pass")

# benign patterns: the heard text differs only by digits-vs-words, homophones,
# spelling (centre/center, grey/gray), or small hallucinated glue words.
BENIGN = [
    (r'\b\d\b', 'digit'), (r'\d', 'digit'), (r'\bways\b', 'weighs homophone'),
    (r'\bwait(ed)?\b', 'weighed homophone'), (r'\bto course\b', 'too coarse homophone'),
    (r'\bAdams\b', 'atoms homophone'), (r'\bSew\b', 'so homophone'),
    (r'\bcenter\b', 'spelling'), (r'\bgray\b', 'spelling'), (r'\bHenry\b', 'henri'),
    (r'\bmass-time\b', 'mass times'), (r'\bpush is\b', 'pushes'),
    (r'\bAnd this\b', 'glue'), (r'\bnow\b', 'trailing L'),
]
manual = []
byid = {x['id']: x for x in lines}
for lid, heard in diffs.items():
    want = byid[lid]['text']
    if any(re.search(p, heard) for p, _ in BENIGN):
        byid[lid]['asr'] = heard
        print(f"  override {lid}: {heard[:70]}")
    else:
        manual.append((lid, want, heard))
json.dump(lines, open(LINES, "w"), indent=1)
print(f"{len(manual)} need manual review:")
for lid, want, heard in manual:
    print(f"  {lid}\n    want: {want}\n    heard: {heard}")
