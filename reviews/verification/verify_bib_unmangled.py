"""Check that add_reviewer3_refs.py only added entries and did not alter existing ones.

Run:  uv run python reviews/verification/verify_bib_unmangled.py

Compares paper/references.bib against its committed version at git HEAD. Parses
each entry into (key, type, {field: value}) with whitespace collapsed, so pure
reformatting is invisible and any change to a field value is not. Exits non-zero
if an existing entry's fields differ, or if an entry disappeared.
"""

import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
BIB = "paper/references.bib"

ENTRY = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,(.*?)\n\}", re.DOTALL)
FIELD = re.compile(r"(\w+)\s*=\s*[{\"](.*?)[}\"]\s*,?\s*(?=\n\s*\w+\s*=|\Z)", re.DOTALL)


def parse(text: str) -> dict[str, tuple[str, dict[str, str]]]:
    out: dict[str, tuple[str, dict[str, str]]] = {}
    for etype, key, body in ENTRY.findall(text):
        fields = {name.lower(): " ".join(value.split())
                  for name, value in FIELD.findall(body)}
        out[key] = (etype.lower(), fields)
    return out


head = subprocess.run(["git", "show", f"HEAD:{BIB}"], cwd=REPO,
                      capture_output=True, text=True, check=True).stdout
now = (REPO / BIB).read_text()

old, new = parse(head), parse(now)
added = sorted(set(new) - set(old))
removed = sorted(set(old) - set(new))
changed = []
for key in sorted(set(old) & set(new)):
    if old[key] != new[key]:
        differing = {f for f in set(old[key][1]) | set(new[key][1])
                     if old[key][1].get(f) != new[key][1].get(f)}
        changed.append((key, sorted(differing)))

print(f"HEAD:  {len(old)} entries")
print(f"now:   {len(new)} entries")
print(f"added:   {added or 'none'}")
print(f"removed: {removed or 'none'}")
if changed:
    print("\nexisting entries whose field values differ:")
    for key, fields in changed:
        print(f"  {key}: {', '.join(fields)}")
        for f in fields:
            print(f"      HEAD: {old[key][1].get(f)!r}")
            print(f"      now : {new[key][1].get(f)!r}")
else:
    print("\nno existing entry changed value; the diff is reformatting plus the additions")

problems = bool(changed or removed)
raise SystemExit(1 if problems else 0)
