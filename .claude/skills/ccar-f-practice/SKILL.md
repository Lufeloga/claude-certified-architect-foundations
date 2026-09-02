---
name: CCAR-F practice runner
description: Sit the CCAR-F practice set on a timer. Presents items one at a time, withholds all feedback until the end by default, then scores by domain against the published blueprint weights and points at the frame that covers the weakest domain.
argument-hint: "[item count, e.g. /ccar-f-practice 20; defaults to 20]"
allowed-tools: Read, AskUserQuestion
---

# CCAR-F practice runner

Run the practice set as a cold, timed sitting.

The default is deliberately austere: no feedback until the end. Immediate
feedback teaches the item, and a cold run measures whether the reasoning
transfers. Offer the coaching mode, but do not make it the default.

**Use only Read and AskUserQuestion.** Read the item bank once, keep the queue
in your own context, and present every item with AskUserQuestion. Do not run
shell commands, do not write scratch files, and do not re-read the bank between
items. A sitting that stops for a permission prompt on every question is not a
sitting, and each of those is avoidable.

## Step 1 · Load the set

Find the item bank. Look for `questions.json` in this order:

1. `practice-set/questions.json` (you are at the repository root)
2. `../practice-set/questions.json` (you are inside a subdirectory)
3. any path the user gave as an argument

If none of those exist, say which paths you tried and ask the user for the path
to their clone of the repository. Do not guess, and do not fall back to reading
`questions.md`, which by design contains no answers.

Each item carries: `id`, `scenario`, `scenario_intro`, `domain`, `task`, `stem`,
`options` (A to D), `key` (a list of letters), `explanations` (one per option),
`why`, and the flags `multi_answer` and `negative`.

## Step 2 · Configure

**If the user passed a number as an argument, ask nothing.** Use that count, all
domains, and feedback at the end, say so in one line, and go straight to the
first item. Somebody who typed `/ccar-f-practice 10` has already told you what
they want.

Only when no argument was given, ask once, as a single question set:

1. **How many items.** Offer 10, 20 (recommended), 30, and the full set.
2. **Which domains.** Offer all domains (recommended), or one of D1 through D5.
3. **Feedback.** Offer "at the end" (recommended) and "after each item".

Then build the queue:

- filter by domain if one was chosen
- vary the order between runs, for example by starting at a different point in
  the bank each time; this needs no tool and no randomness source
- take the requested count
- when the user asked for all domains and enough items, sample so the domain
  mix approximates the blueprint weights below, rather than taking the first N
  at random

Before the first item, state the time budget and hand timing to the user:

> The full set is written for 120 minutes, about two minutes an item. Start your
> own timer now if you want one.

You cannot measure elapsed time between turns, so never report a duration and
never estimate one. Saying how long the sitting should take is useful; inventing
how long it did take is not.

## Step 3 · Run

For each item, in order:

1. Print a progress line: `Item N of TOTAL`. Never show a running score, which
   turns a diagnostic into a performance.
2. Present the scenario intro **only when the scenario changes** from the
   previous item, so it is not repeated ten times.
3. Ask with AskUserQuestion: one question, four options labeled A to D, each
   option carrying the full text from the bank. One call per item, and nothing
   else between items.
   - When `multi_answer` is true, say **Select two** above the question and
     accept two selections.
   - When `negative` is true, present the stem exactly as written. Do not add
     emphasis, do not warn that it is a negative item, and do not restate it in
     the positive. Reading the stem carefully is the thing being exercised.
4. Record the answer. Do not reveal anything.
5. If feedback was set to "after each item", state whether it was right, give
   the correct letters, and print the explanation for the option the user chose
   plus the explanation for the key. If it was set to "at the end", acknowledge
   and move on with no signal either way.

Never reveal a key before the user has answered that item. Never skip or
truncate an item mid-run. Never interrupt the run with anything that needs the
user's approval.

## Step 4 · Score

An item counts as correct only when the selected letters match the key exactly;
a multi-answer item with one of two right is wrong.

**How you report depends on how many items were answered, because a rate needs
a sample and a short run does not have one.** Ten items spread across five
domains give two items each, and no percentage computed from two items means
anything. Reporting one anyway is the error the whole set was rebuilt to avoid.

### Fewer than 25 items answered: no percentages at all

```
Items          C / N

Misses by frame
  Output Reliability          2
  Orchestration               1
  Configuration Placement     1
```

Count each missed item under the frame that covers it, using the table in step
5. Report counts, never percentages, and never a per-domain figure. A run this
size produces a direction, not a measurement, and the report should look like a
direction.

### 25 items or more: the domain breakdown

```
Items          C / N  (P%)

By domain
  D1  Agentic Architecture & Orchestration     c/n  (p%)
  D2  Tool Design & MCP Integration            c/n  (p%)
  D3  Claude Code Configuration & Workflows    c/n  (p%)
  D4  Prompt Engineering & Structured Output   c/n  (p%)
  D5  Context Management & Reliability         c/n  (p%)
```

Show only domains that appeared. For any domain with fewer than five items
answered, print `too few items` in place of a percentage.

**In both modes, do not report a scaled score and do not print a pass or fail
verdict.** The scoring scale belongs to the certification, and a number from a
practice set that looks like an official one invites a false conclusion in
either direction.

## Step 5 · Point somewhere

List every missed item as: number, the correct letters, and its `why` line.

Then name one frame to read, and only one:

- **Short run:** the frame with the most misses. On a tie, take the frame whose
  misses came from more than one scenario, since a pattern that survives a
  change of setting is the more useful signal.
- **Long run:** the frame covering the weakest domain among those with five or
  more items.

| Domain | Frame in `frame-map/README.md` |
|---|---|
| D1 | Orchestration, and Execution Mode |
| D2 | Output Reliability |
| D3 | Configuration Placement |
| D4 | Output Reliability |
| D5 | Context & State, and Human Escalation |

Close by suggesting a re-run scoped to that domain once they have read it.

## Reference

Blueprint weights, for the sampling in step 2:
D1 27%, D3 20%, D4 20%, D2 18%, D5 15%.

## Rules

- Keep everything outside the questions themselves short. This is a sitting, not
  a conversation.
- Read the bank once and never again. Everything after that is in context.
- Do not coach, hint, or narrate reasoning while items are being answered.
- Do not editorialize about difficulty before or during the run.
- If the user abandons partway, score what was answered and say how many items
  were left.
