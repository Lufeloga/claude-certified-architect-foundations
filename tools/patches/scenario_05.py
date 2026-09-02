"""Scenario 5 rewrite: Claude Code for Continuous Integration (items 41-50)."""

PATCH = {
    41: {
        "domain": "D3",
        "task": "3.6",
        "guide_anchor": "3.6 Skills in: running Claude Code in CI with the -p flag; using --output-format json with --json-schema to produce machine-parseable structured findings for automated posting as inline PR comments",
        "stem": (
            "A nightly job must run the assistant without any interaction and emit machine-readable "
            "findings that a later step posts automatically as inline comments. Which invocation "
            "is correct?"
        ),
        "options": {
            "A": "Set a headless environment variable and parse the standard output.",
            "B": "Run with a batch flag and read the aggregated results file it writes.",
            "C": "Run with `-p`, `--output-format json`, and `--json-schema` for the shape.",
            "D": "Run interactively in the container and capture the terminal output.",
        },
        "key": ["C"],
        "explanations": {
            "A": "There is no such environment variable, and parsing free-form output is what structured output exists to replace.",
            "B": "There is no batch flag on the CLI; batching is a property of the API, not of a Claude Code invocation.",
            "C": "Non-interactive mode prevents the hang, and the two output flags together produce findings a later step can post without parsing prose.",
            "D": "Running interactively in CI is what hangs the job waiting for input that never arrives.",
        },
        "distractor_families": {
            "A": "invented artifact",
            "B": "invented artifact",
            "D": "the failure mode the flag exists to prevent",
        },
        "why": "Non-interactive plus a declared schema is what makes CI output usable downstream.",
    },
    42: {
        "domain": "D3",
        "task": "3.6",
        "guide_anchor": "3.6 Knowledge of: session context isolation: why the same Claude session that generated code is less effective at reviewing its own changes compared to an independent review instance",
        "stem": (
            "The pipeline reviews several pull requests within one run, and reviewers notice "
            "comments on one pull request that reference code belonging to another. Each review "
            "on its own is accurate. What should the pipeline do?"
        ),
        "options": {
            "A": "Clear the context between pull requests inside the same session.",
            "B": "Run each pull request in a session isolated from the others.",
            "C": "Reduce how many pull requests are handled in a single run.",
            "D": "Instruct the agent to consider only the current diff each time.",
        },
        "key": ["B"],
        "explanations": {
            "A": "Clearing inside one session depends on the clearing being complete every time, which is a weaker guarantee than never sharing the context at all.",
            "B": "Separate sessions make cross-contamination structurally impossible rather than something the pipeline has to remember to prevent.",
            "C": "Fewer pull requests per run reduces how often the bleed happens without removing the cause.",
            "D": "An instruction asks the model not to use context that is still sitting in front of it.",
        },
        "distractor_families": {
            "A": "right direction, weaker guarantee",
            "C": "reduces exposure, not cause",
            "D": "prompt where isolation is required",
        },
        "why": "Isolation by construction beats an instruction to ignore what is present.",
    },
    43: {
        "domain": "D3",
        "task": "3.6",
        "guide_anchor": "3.6 Skills in: including prior review findings in context when re-running reviews after new commits, instructing Claude to report only new or still-unaddressed issues to avoid duplicate comments",
        "stem": (
            "When the review re-runs after new commits, it posts duplicate comments on issues that "
            "were already raised and discussed in the thread. The findings themselves are "
            "accurate. What should change?"
        ),
        "options": {
            "A": "Supply the prior findings and ask for new or unaddressed issues only.",
            "B": "Review only the diff introduced by the most recent commit each time.",
            "C": "Deduplicate the comments after they have been posted to the thread.",
            "D": "Run the review a single time, when the pull request is first opened.",
        },
        "key": ["A"],
        "explanations": {
            "A": "The agent repeats itself because each run starts blind; giving it the prior findings is what lets it tell new from already-said.",
            "B": "Restricting to the latest diff hides issues that earlier commits introduced and later commits never touched.",
            "C": "Post-hoc deduplication cleans the thread after the noise has already reached the developers.",
            "D": "Reviewing once abandons the point of re-running, which is to catch what the new commits introduce.",
        },
        "distractor_families": {
            "B": "narrows scope and loses coverage",
            "C": "band-aid downstream",
            "D": "removes the capability instead of fixing it",
        },
        "why": "An agent cannot avoid repeating what it was never told it already said.",
    },
    44: {
        "domain": "D3",
        "task": "3.6",
        "guide_anchor": "3.6 Skills in: providing existing test files in context so test generation avoids suggesting duplicate scenarios already covered by the test suite",
        "stem": (
            "Generated tests frequently duplicate scenarios the existing suite already covers. The "
            "duplicated tests are themselves correct and they pass. What addresses this?"
        ),
        "options": {
            "A": "Ask for a smaller number of generated tests on each run.",
            "B": "Filter out duplicates after the generation step completes.",
            "C": "Generate tests only for files that currently have no coverage.",
            "D": "Provide the existing test files in context during generation.",
        },
        "key": ["D"],
        "explanations": {
            "A": "Fewer tests means proportionally fewer duplicates and proportionally fewer new ones too.",
            "B": "Filtering afterwards spends the generation on work that is discarded and needs a reliable equivalence check.",
            "C": "File-level coverage is too coarse: a covered file can still have uncovered branches, which is where the useful tests are.",
            "D": "Once the agent can see what the suite already asserts, it stops proposing it.",
        },
        "distractor_families": {
            "A": "reduces volume, not redundancy",
            "B": "band-aid downstream",
            "C": "wrong granularity",
        },
        "why": "The agent duplicates what it cannot see.",
    },
    45: {
        "domain": "D3",
        "task": "3.6",
        "guide_anchor": "3.6 Skills in: documenting testing standards, valuable test criteria, and available fixtures in CLAUDE.md to improve test generation quality and reduce low-value test output",
        "stem": (
            "The tests the CI job generates are low value: trivial assertions, the wrong fixtures, "
            "and coverage of paths nobody cares about. The job invocation and output handling are "
            "both correct. What is the most effective change?"
        ),
        "options": {
            "A": "Document the standards, what makes a test valuable, and the fixtures.",
            "B": "Add few-shot examples of well-written tests to the prompt used in CI.",
            "C": "Raise the model tier the continuous integration job runs against.",
            "D": "Have a second instance review the generated tests before they land.",
        },
        "key": ["A"],
        "explanations": {
            "A": "All three symptoms are missing project knowledge, and the always-loaded project file is where CI-invoked runs pick that knowledge up.",
            "B": "Examples are strong for format and for ambiguous judgment calls, but they cannot tell the agent which fixtures this repository has.",
            "C": "A stronger model still cannot know which paths this team considers worth covering.",
            "D": "Review catches bad tests after they are written rather than causing better ones to be written.",
        },
        "distractor_families": {
            "B": "two-valid-one-superior: right technique, cannot supply the missing facts",
            "C": "irrelevant lever",
            "D": "inspection instead of specification",
        },
        "why": "Quality complaints that are really missing context get fixed by supplying the context.",
    },
    46: {
        "domain": "D3",
        "task": "3.5",
        "guide_anchor": "3.5 Knowledge of: test-driven iteration: writing test suites first, then iterating by sharing test failures to guide progressive improvement",
        "stem": (
            "A module has a suite of assertions that already define its expected behavior, "
            "including its edge cases, and the implementation is now being written against them. "
            "Which refinement technique fits?"
        ),
        "options": {
            "A": "Iterate by sharing the failing tests until the suite passes.",
            "B": "Provide two or three input and output examples to work from.",
            "C": "Have the agent interview the team about the module's design.",
            "D": "Enter plan mode before any implementation code is written.",
        },
        "key": ["A"],
        "explanations": {
            "A": "The suite already encodes the specification, so each failure is a precise, checkable instruction for the next iteration.",
            "B": "Examples communicate a transformation when no executable specification exists; here one already does, in more detail.",
            "C": "An interview surfaces requirements nobody has stated, and the edge cases are stated already.",
            "D": "Plan mode weighs approaches, and the approach here is to satisfy an existing suite.",
        },
        "distractor_families": {
            "B": "weaker form of a specification already present",
            "C": "elicits what is already written down",
            "D": "deliberation where the target is fixed",
        },
        "why": "When the specification is executable, failures are the feedback loop.",
    },
    47: {
        "domain": "D4",
        "task": "4.5",
        "guide_anchor": "4.5 Knowledge of: batch processing is appropriate for non-blocking, latency-tolerant workloads and inappropriate for blocking workflows; the batch API does not support multi-turn tool calling within a single request",
        "stem": (
            "The pipeline runs two workloads. A pre-merge check blocks the merge and requires the "
            "agent to call repository tools while it reasons. A weekly audit of the whole "
            "repository is read on Monday mornings and is submitted the preceding Friday. How "
            "should each be run?"
        ),
        "options": {
            "A": "Both with the batch API, since both are bounded and repeatable jobs.",
            "B": "Both synchronously, because batch carries no guaranteed latency floor.",
            "C": "Pre-merge with batch at pull request open, and the audit synchronously.",
            "D": "Pre-merge synchronously, and the weekly audit with the batch API.",
        },
        "key": ["D"],
        "explanations": {
            "A": "The pre-merge check fails two batch preconditions at once: it blocks a person, and it needs tool calls inside a single request.",
            "B": "Running the weekly audit synchronously is correct but pays full price for a job with three days of slack.",
            "C": "This is the correct reasoning applied to the wrong workload, and the batch limitation on mid-request tool calls makes the pre-merge check unrunnable.",
            "D": "The blocking, tool-calling workload goes synchronous; the latency-tolerant one takes the savings.",
        },
        "distractor_families": {
            "A": "ignores the blocking constraint",
            "B": "safe but leaves savings on the table",
            "C": "assignments inverted",
        },
        "why": "Batch suits work nobody is waiting on and that needs no tools mid-request.",
    },
    48: {
        "domain": "D4",
        "task": "4.6",
        "guide_anchor": "4.6 Knowledge of: self-review limitations: a model retains reasoning context from generation, making it less likely to question its own decisions in the same session; independent review instances are more effective than self-review instructions or extended thinking",
        "negative": True,
        "stem": (
            "The team wants to catch subtle defects in code the same pipeline generated earlier in "
            "the run. Which approach is least effective?"
        ),
        "options": {
            "A": "Reviewing in a separate instance that lacks the generation context.",
            "B": "Having the generating session review its own output while thinking.",
            "C": "Splitting the review into per-file passes plus a cross-file pass.",
            "D": "Having the review self-report confidence per finding for triage.",
        },
        "key": ["B"],
        "explanations": {
            "A": "An instance without the generator's reasoning has no commitment to the decisions it is inspecting.",
            "B": "The session that produced the code carries the reasoning that made it look right, and more deliberation inside that same context does not dislodge it.",
            "C": "Splitting the passes addresses attention dilution, which is a different failure and a real one.",
            "D": "Per-finding confidence does not catch defects by itself, but it routes maintainer attention usefully.",
        },
        "distractor_families": {
            "A": "the recommended approach offered as if weak",
            "C": "valid technique for a neighboring problem",
            "D": "valid triage aid",
        },
        "why": "Self-review inherits the reasoning that produced the defect.",
    },
    49: {
        "domain": "D4",
        "task": "4.1",
        "guide_anchor": "4.1 Knowledge of: how general instructions like 'be conservative' or 'only report high-confidence findings' fail to improve precision compared to specific categorical criteria",
        "stem": (
            "The review reports 14 findings per pull request and developers act on 4. The noise is "
            "concentrated in style-adjacent observations about patterns that are established "
            "conventions in this repository. A developer proposes adding \"only report "
            "high-confidence issues\" to the prompt. What is the most effective change?"
        ),
        "options": {
            "A": "Add the proposed instruction, since it directly targets over-reporting.",
            "B": "Have the agent critique its findings and drop the ones it cannot justify.",
            "C": "Name explicitly which issue classes to report and which ones to skip.",
            "D": "Attach a confidence score to each finding and suppress the low ones.",
        },
        "key": ["C"],
        "explanations": {
            "A": "Confidence is not the problem: the agent is highly confident about style observations that this team simply does not want.",
            "B": "Self-critique helps where the gaps vary unpredictably; here the unwanted class is stable and nameable, so it can just be excluded.",
            "C": "The noise falls in one identifiable category, and a criterion that names it removes the category without touching the findings developers act on.",
            "D": "A numeric threshold is the same confidence filter in numeric clothing, and it drops accurate findings alongside unwanted ones.",
        },
        "distractor_families": {
            "A": "intensity dial in place of a criterion",
            "B": "right technique, wrong trigger",
            "D": "false proxy: confidence for relevance",
        },
        "why": "If you can name the category you do not want, name it instead of tuning a dial.",
    },
    50: {
        "domain": "D4",
        "task": "4.3",
        "guide_anchor": "4.3 Knowledge of: tool use with JSON schemas as the most reliable approach for guaranteed schema-compliant structured output; 3.6 --output-format json and --json-schema for enforcing structured output in CI",
        "select_instruction": "Select two",
        "stem": (
            "The continuous integration job must decide automatically whether to block a merge. "
            "Which two approaches produce output the pipeline can rely on?"
        ),
        "options": {
            "A": "Ask for JSON in the prompt and parse the model's text output.",
            "B": "Define a tool whose input is the verdict schema and read `tool_use`.",
            "C": "Have the agent write prose and search it for a verdict keyword.",
            "D": "Run headless with `--output-format json` and a declared verdict schema.",
        },
        "key": ["B", "D"],
        "multi_answer": True,
        "explanations": {
            "A": "Asking for JSON in prose produces JSON most of the time, and a pipeline that blocks merges cannot run on most of the time.",
            "B": "A schema attached to a tool makes the response structurally conformant instead of hopefully conformant.",
            "C": "Keyword search over prose is the least reliable option here: a single hedged sentence flips the verdict.",
            "D": "The CLI flags enforce the same guarantee at the invocation level, which is where a pipeline consumes it.",
        },
        "distractor_families": {
            "A": "request instead of enforcement",
            "C": "parsing prose for a decision",
        },
        "why": "A schema enforces the shape; a prompt only requests it.",
    },
}
