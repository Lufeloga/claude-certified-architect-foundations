# Practice runner skill

A Claude Code skill that runs the practice set cold and on a timer, scores by
domain, and points you at the frame covering your weakest one.

## Install

From the repository root:

```bash
mkdir -p .claude/skills
cp skill/ccar-f-practice.skill .claude/skills/
```

To have it available in every project instead of this one, copy it to
`~/.claude/skills/` and it follows you rather than the repository.

## Run

```
/ccar-f-practice        # 20 items
/ccar-f-practice 10     # a short sitting
/ccar-f-practice 60     # the full set
```

It asks how many items, which domains, and whether you want feedback as you go
or only at the end.

## What it does

**No feedback until the end, by default.** Immediate feedback teaches you the
item. A cold run tells you whether the reasoning transfers, which is the thing
worth knowing. The coaching mode is there when you want it, but it is not the
default.

**It times you.** The full set is written for 120 minutes.

**It scores by domain**, weighted to the published blueprint, and stays quiet
about any domain with fewer than five items answered rather than reporting a
percentage that will be over-read.

**It does not report a scaled score or a pass/fail verdict.** The scale belongs
to the certification, and a number from a practice set that looks like an
official one invites a false conclusion in either direction. The domain
breakdown is the part that tells you what to do next.

**It routes you somewhere.** Your weakest domain maps to a frame in the
[Frame Map](../frame-map/), and it names which one to read.

## How it reads the set

The skill reads [`practice-set/questions.json`](../practice-set/questions.json),
which is the source of truth for every format in this repository. Edit that file
and the skill picks up the change with no rebuild.
