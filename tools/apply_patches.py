#!/usr/bin/env python3
"""Apply scenario rewrite patches to questions.json.

Each patch module in tools/patches/ exports PATCH: {item_id: {field: value}}.
Fields are merged over the existing item, so a patch can touch one field or all
of them. Applying is idempotent: running twice produces the same file.

Usage:  python3 tools/apply_patches.py [scenario_01 scenario_02 ...]
        with no arguments, every patch module in tools/patches/ is applied.
"""

import importlib.util
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
QUESTIONS = ROOT / "practice-set" / "questions.json"
PATCH_DIR = ROOT / "tools" / "patches"


def load_patch(name: str) -> dict:
    path = PATCH_DIR / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.PATCH


def main() -> int:
    names = sys.argv[1:] or sorted(p.stem for p in PATCH_DIR.glob("scenario_*.py"))
    data = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    by_id = {i["id"]: i for i in data["items"]}

    touched = 0
    for name in names:
        patch = load_patch(name)
        for item_id, fields in patch.items():
            if item_id not in by_id:
                print(f"  !! {name}: no item {item_id}", file=sys.stderr)
                continue
            item = by_id[item_id]
            for field, value in fields.items():
                item[field] = value
            item["multi_answer"] = len(item["key"]) > 1
            # The legacy single-paragraph rationale is superseded once an item
            # carries a per-option explanation.
            if item.get("explanations"):
                item.pop("rationale_legacy", None)
            touched += 1
        print(f"{name}: {len(patch)} items")

    data["items"] = [by_id[i] for i in sorted(by_id)]
    data["item_count"] = len(data["items"])
    QUESTIONS.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    done = sum(1 for i in data["items"] if i.get("guide_anchor"))
    print(f"\n{touched} items patched. {done}/{len(data['items'])} now anchored to the guide.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
