# Changelog

Item-level changes to the practice set, so anyone who has already sat it knows
what to re-check.

The set carries a `set_version` in `questions.json`.

- **Minor** rises when wording, an explanation, or a typo changes.
- **Major** rises when a key changes or an item is withdrawn. If you sat the set
  under a previous major version, the entries below are the ones to revisit.

## Unreleased

- The runner reports counts and a frame to read on runs under 25 items, instead
  of per-domain percentages computed from two or three answers.
- It states the time budget and leaves the clock to the reader, rather than
  reporting a duration it cannot measure.

## 1.0.0

First public release.

- 60 items across the six scenarios in the published blueprint, weighted to
  match it: D1 16, D3 12, D4 12, D2 11, D5 9.
- Every option rewritten so that option length carries no signal. A program
  always choosing the longest option went from 72.2% correct to 25.9%, against
  25% chance. See [QUALITY.md](QUALITY.md).
- The six multi-answer items were re-lettered to six distinct pairs. Five of six
  had been keyed A+C, which was guessable.
- Every item gained an explanation for each of its four options, a named
  distractor family for each wrong one, a closing rationale, and a citation to
  the Exam Guide line its key rests on.
- Questions and answers split into separate files so the set can be sat cold.
- Five items asking which option is weakest are presented as reasoning practice,
  with no claim about which formats the certification exam uses.
