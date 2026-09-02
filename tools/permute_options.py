#!/usr/bin/env python3
"""Reorder an item's options, carrying the key and every per-option field with it.

Rewriting options to a uniform length removes the length tell but can introduce
a positional one: while rebalancing, all six multi-answer items ended up keyed
B+D. Permuting is how position is spread without touching any wording, so the
content stays exactly as reviewed.

Usage:  python3 tools/permute_options.py 7:CADB 19:BADC ...
        where the mapping lists, for new positions A B C D, the old letter that
        moves there. 7:CADB means new A is old C, new B is old A, and so on.
"""

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
QUESTIONS = ROOT / "practice-set" / "questions.json"
LETTERS = "ABCD"
PER_OPTION = ("options", "explanations", "distractor_families")


def permute(item: dict, order: str) -> None:
    """order[i] is the old letter that becomes LETTERS[i]."""
    if sorted(order) != list(LETTERS):
        raise ValueError(f"item {item['id']}: {order!r} is not a permutation of ABCD")
    old_to_new = {old: LETTERS[i] for i, old in enumerate(order)}
    for field in PER_OPTION:
        current = item.get(field) or {}
        item[field] = {
            old_to_new[old]: value for old, value in current.items() if old in old_to_new
        }
        # Keep the letters in reading order so the JSON stays reviewable.
        item[field] = {l: item[field][l] for l in LETTERS if l in item[field]}
    item["key"] = sorted(old_to_new[l] for l in item["key"])


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    data = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    by_id = {i["id"]: i for i in data["items"]}

    for spec in sys.argv[1:]:
        raw_id, _, order = spec.partition(":")
        item = by_id[int(raw_id)]
        before = "".join(item["key"])
        permute(item, order.upper())
        print(f"item {item['id']:>2}: key {before} -> {''.join(item['key'])}")

    QUESTIONS.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
