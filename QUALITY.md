# Quality audit

Every claim this repository makes about the practice set is measurable, and the
scripts that measure it are in [tools/](tools/). Run them yourself:

```bash
python3 tools/audit_keys.py
python3 tools/heuristic_solver.py
```

This page reports what they returned before and after the set was rebuilt.

## The problem this found

A multiple-choice set is only a diagnostic if reading the question is the
cheapest way to answer it. If the key is reliably the longest option, or the
only one naming a real artifact, then a candidate who has learned nothing can
still score well, and the domain breakdown they take away is meaningless.

So the set is attacked by a program that answers using only surface features of
the options, with no understanding of the material at all. Each strategy is a
shortcut real test-takers use.

**On the first draft of this set, always choosing the longest option scored
72.2%.** Sixty items, no reading, seventy-two percent. That is the single worst
defect the audit found, and it existed because writing a good key invites
elaboration while a distractor gets a short sentence.

## Blind heuristic attack

Chance on a four-option item is 25%. The threshold for a passing verdict is 35%.
Strategies that abstain on most items are reported as INSUFFICIENT rather than
scored: one lucky hit out of two attempts reads as 50% and means nothing.

| Strategy | Before | After |
|---|---|---|
| Longest option | **72.2%** (39/54) | **25.9%** (14/54) |
| Shortest option | 9.3% (5/54) | 27.8% (15/54) |
| Most stem overlap | 22.2% (6/27) | 33.3% (10/30) |
| Most hedged wording | 23.8% (5/21) | 11.8% (2/17) |
| Most technical tokens | 70.0% (7/10) | insufficient (2/6) |
| Fewest absolutes | insufficient (0/1) | insufficient (1/2) |
| **Combined vote** | **54.5%** (12/22) | **32.0%** (8/25) |

The worst scored strategy is now 33.3%, against 25% chance.

Both directions are tracked on purpose. Trimming the correct answers would have
fixed the first row and created the same exploit in reverse, since "the long one
is a trap" is a rule a reader can learn just as easily. The fix was to give the
distractors real specificity instead, which raises difficulty and removes the
signal in the same edit.

## Answer key audit

| Check | Before | After |
|---|---|---|
| Letter distribution, single-answer | A 13 · B 13 · C 13 · D 15 | unchanged |
| Multi-answer pairs distinct | **2 of 6** (five were A+C) | **6 of 6** |
| Key is the longest option | **72.2%** | 25.9% |
| Key is the shortest option | 9.3% | 27.8% |
| Mean length, key vs distractor | **+17.5 characters** | **-0.2** |
| Longest run of one key letter | 3 | 3 |
| Explanation for every option | **0 of 60** | **60 of 60** |
| Closing rationale per item | **0 of 60** | **60 of 60** |
| Cites the guide line behind its key | **0 of 60** | **60 of 60** |

All 13 checks pass.

## Coverage

Item counts follow the published blueprint weights, so a domain percentage from
this set is comparable to the weight that domain carries.

| Domain | Blueprint weight | Items | Share |
|---|---|---|---|
| D1 · Agentic Architecture & Orchestration | 27% | 16 | 27% |
| D3 · Claude Code Configuration & Workflows | 20% | 12 | 20% |
| D4 · Prompt Engineering & Structured Output | 20% | 12 | 20% |
| D2 · Tool Design & MCP Integration | 18% | 11 | 18% |
| D5 · Context Management & Reliability | 15% | 9 | 15% |

Ten items per scenario across the six scenarios named in the blueprint.

## What the audit does not measure

**Whether the answers are right.** No script can check that. What the rebuild
added instead is a `guide_anchor` on all 60 items, naming the specific
*Knowledge of* or *Skills in* line the key rests on. That does not prove an item
correct, but it makes disagreement resolvable: two citations can be compared,
two opinions cannot.

**Whether all four options are genuinely defensible.** This was reviewed item by
item and it remains a judgment made by the person who wrote them, which is a
weak guarantee. The blind solver exists precisely because that judgment could
not be trusted on its own, and it caught a 72% leak the author had not noticed.

**Whether the difficulty matches the certification exam.** It cannot, and no
claim is made either way. The exam is under NDA and nothing here is derived from
sitting it.

## Defects found in this material, and fixed

Recorded because the list is more useful than the assurance.

1. **The length tell.** 72.2% of items had the key as the longest option.
2. **Multi-answer pairs were guessable.** Five of six were keyed A+C.
3. **Artifact concentration.** Options naming an artifact in backticks were
   disproportionately the key, at 70% on the items where it applied.
4. **A defect introduced during the fix.** Rebalancing the six multi-answer
   items one at a time left all six keyed B+D. Check B2 caught it, and the
   options were re-lettered without any wording changing.
5. **No per-option explanations.** Every item had a single paragraph. The reason
   a plausible option fails is the part worth learning, so each option now
   carries its own.
6. **Claims about the exam's behavior.** Earlier drafts asserted things about
   how the certification exam behaves. Those are removed. This material
   describes itself and cites the published guide, nothing else.
7. **Mixed spelling conventions.** British and American spellings appeared in
   the same document set. `tools/lint_prose.py` now enforces one.
8. **A dead link to the official Exam Guide.** The single most important
   outbound link in the repository pointed at a page that returns 404. It was
   written from memory and never opened. `tools/check_links.py` now resolves
   every link in every document.

## Reproducing this

```bash
python3 tools/build.py             # regenerate every format from questions.json
python3 tools/audit_keys.py        # 13 structural and statistical checks
python3 tools/heuristic_solver.py  # the blind attack above
python3 tools/lint_prose.py        # spelling, terminology, personal data
python3 tools/check_links.py       # every link resolves
```

All five must pass before a change is merged, and none of them needs anything
beyond Python 3.
