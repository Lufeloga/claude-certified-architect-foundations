# Contributing

The most valuable contribution is telling me an answer is wrong.

## Reporting a wrong or arguable key

Open an issue with:

1. **The item number.**
2. **The answer you believe is correct**, and why.
3. **The line of the official Exam Guide that supports it.** Quote the *Knowledge
   of* or *Skills in* bullet.

That third point is what makes the discussion resolvable. Every item in this set
carries a `guide_anchor` field naming the line its key rests on, so a
disagreement becomes a comparison of two citations rather than two opinions.

If the guide genuinely does not settle it, the item is ambiguous and should be
rewritten or withdrawn. That is a useful finding too.

## Reporting a leaky item

If you can answer an item without understanding it, say so. Useful reports name
the shortcut: the key is the only option mentioning a real artifact, the
distractors all use absolutes, the correct answer echoes the stem.

`tools/heuristic_solver.py` automates the shortcuts already known. A shortcut it
does not model is worth adding to it.

## Editing the material

**`practice-set/questions.json` is the only file to edit.** The Markdown, the
HTML, and the PDF are generated. A pull request that edits `questions.md`
directly will be reverted by the next build.

After editing, run all four:

```bash
python3 tools/build.py
python3 tools/audit_keys.py
python3 tools/heuristic_solver.py
python3 tools/lint_prose.py
```

All four must pass before a change is merged. They have no dependencies beyond
Python 3.

## House rules for new or rewritten items

- Every option must be defensible by someone who knows the material. If one can
  be dismissed without thinking, the item teaches nothing.
- The clause that decides the answer belongs in the middle of the stem. If the
  item can be answered from its last line alone, it is telegraphing.
- Option length must carry no information. The audit tracks this in both
  directions, because "the long one is a trap" is just as exploitable as the
  reverse.
- Every option gets its own explanation, and each wrong one names why it fails
  as a principle, not just that it is wrong.
- Every item cites the guide line its key rests on. No citation, no item.
- Nothing is keyed to behavior the published guide does not describe.

## Scope

This covers the CCAR-F certification. Generalizing the framework to other exams
is out of scope, as is reproducing any part of the official Exam Guide.

## License

Contributions are accepted under [CC BY 4.0](LICENSE), the same terms as the
rest of the repository.
