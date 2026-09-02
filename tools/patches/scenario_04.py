"""Scenario 4 rewrite: Developer Productivity with Claude (items 31-40)."""

PATCH = {
    31: {
        "domain": "D2",
        "task": "2.5",
        "guide_anchor": "2.5 Skills in: selecting Glob for finding files matching naming patterns (e.g., **/*.test.tsx)",
        "stem": (
            "A job must run against every component test file in the monorepo. The convention is a "
            "`.test.tsx` suffix, three legacy directories still use `.spec.tsx`, and some test "
            "files import shared helpers while others define their own. What produces the "
            "complete list most reliably?"
        ),
        "options": {
            "A": "Grep for `describe(` and collect the files that contain a match.",
            "B": "Glob for `**/*.test.tsx` and `**/*.spec.tsx`, then merge the two.",
            "C": "Grep for imports of the shared helpers and collect those files.",
            "D": "Glob for `**/*.tsx` and read each file to decide what it is.",
        },
        "key": ["B"],
        "explanations": {
            "A": "Searching for a test function name finds files by their contents, which misses any suite written with a different harness and catches non-test files that mention it.",
            "B": "Both naming conventions are file path patterns, so two globs cover the whole population exactly.",
            "C": "The scenario states some test files define their own helpers, so this misses them by construction.",
            "D": "Reading every `.tsx` file in a monorepo to classify it works, at a cost far above matching two patterns.",
        },
        "distractor_families": {
            "A": "content search for a path problem",
            "C": "criterion the scenario already excludes",
            "D": "correct but grossly inefficient",
        },
        "why": "Finding files by name is a Glob question; Grep answers questions about contents.",
    },
    32: {
        "domain": "D2",
        "task": "2.5",
        "guide_anchor": "2.5 Knowledge of: when Edit fails due to non-unique text matches, using Read + Write as a fallback for reliable file modifications",
        "stem": (
            "A configuration constant appears in seven places in one file, and only the occurrence "
            "inside the staging block should change. The `Edit` call fails because the target "
            "text is not unique. What do you do?"
        ),
        "options": {
            "A": "Extend the search text with surrounding lines until the match is unique.",
            "B": "Use a replace-all edit and then revert the six unintended changes.",
            "C": "Read the file, change the intended occurrence, and write it back whole.",
            "D": "Append the corrected constant at the end so the later value wins.",
        },
        "key": ["C"],
        "explanations": {
            "A": "Widening the anchor sometimes works and is worth a try, but it depends on the surrounding lines happening to differ, which seven repetitions in one file make unlikely.",
            "B": "Making six wrong changes in order to make one right one leaves the file correct only if every revert lands.",
            "C": "Reading the full contents and writing them back is the documented fallback precisely because it does not depend on a unique anchor existing.",
            "D": "Appending a duplicate definition changes behavior through shadowing rather than editing the value that was meant to change.",
        },
        "distractor_families": {
            "A": "two-valid-one-superior: works only if the file cooperates",
            "B": "damage-then-repair",
            "D": "side effect standing in for an edit",
        },
        "why": "When Edit has no unique anchor, Read plus Write is the reliable path.",
    },
    33: {
        "domain": "D2",
        "task": "2.5",
        "guide_anchor": "2.5 Skills in: tracing function usage across wrapper modules by first identifying all exported names, then searching for each name across the codebase",
        "stem": (
            "You need every call site of `validateToken`, which is exported from `auth/core.ts` "
            "and re-exported under different names by three wrapper modules. The wrappers "
            "themselves are documented and correct. What is the correct first move?"
        ),
        "options": {
            "A": "Grep for `validateToken` repository-wide and compile the matches found.",
            "B": "Glob for the files under `auth/` and read each one of them in turn.",
            "C": "Read the library and wrappers for every exported name, then search each.",
            "D": "Grep for imports of `auth/core` and trace outward from those files.",
        },
        "key": ["C"],
        "explanations": {
            "A": "Searching the original name finds only the callers that use it, and the wrappers exist precisely to expose other names.",
            "B": "The callers are spread across the codebase; reading the `auth/` directory describes the source, not its consumers.",
            "C": "Enumerating the aliases first turns one incomplete search into a complete set of searches.",
            "D": "Import tracing finds the wrappers themselves, then stops one hop short of the code that calls them by their new names.",
        },
        "distractor_families": {
            "A": "single-name search under aliasing",
            "B": "explores the definition, not the usage",
            "D": "stops one hop short",
        },
        "why": "Enumerate the aliases before searching, or the search is incomplete by construction.",
    },
    34: {
        "domain": "D2",
        "task": "2.5",
        "guide_anchor": "2.5 Skills in: building codebase understanding incrementally: starting with Grep to find entry points, then using Read to follow imports and trace flows, rather than reading all files upfront",
        "stem": (
            "You must understand how retry backoff is reached in an unfamiliar 28-file service "
            "before changing it. The whole service fits comfortably inside your context window. "
            "Which approach fits best?"
        ),
        "options": {
            "A": "Read all 28 files in order so nothing in the service is missed.",
            "B": "Glob for the files whose names reference retry or backoff logic.",
            "C": "Delegate the survey to a subagent and work from the report it returns.",
            "D": "Grep the retry entry points, read those, and follow their imports.",
        },
        "key": ["D"],
        "explanations": {
            "A": "Reading everything fits here, but it spends the whole window on a question about one flow and buries the answer in unrelated material.",
            "B": "File names are a weak proxy for behavior, and backoff logic frequently lives in files named for something else.",
            "C": "Delegation earns its overhead when the material will not fit; the scenario states that it does.",
            "D": "Finding the entry points and following imports traces the actual path through the service, which is the thing being asked about.",
        },
        "distractor_families": {
            "A": "exhaustive where targeted is better",
            "B": "names as a proxy for behavior",
            "C": "right technique, precondition denied",
        },
        "why": "Trace the flow from its entry points instead of ingesting the whole service.",
    },
    35: {
        "domain": "D3",
        "task": "3.1",
        "guide_anchor": "3.1 Skills in: using the /memory command to verify which memory files are loaded and diagnose inconsistent behavior across sessions",
        "stem": (
            "Two engineers working in the same repository, on the same version, get noticeably "
            "different behavior from the assistant. Both have pulled the latest commit. What is "
            "the first step to diagnose it?"
        ),
        "options": {
            "A": "Check which memory files each session has actually loaded.",
            "B": "Compare their user-level settings files line by line for drift.",
            "C": "Have both re-clone the repository to rule out a stale checkout.",
            "D": "Consolidate every project convention into one `CLAUDE.md` file.",
        },
        "key": ["A"],
        "explanations": {
            "A": "Different behavior on identical code means different instructions are in play, and listing what each session loaded shows that directly.",
            "B": "User-level files are one plausible source of the difference, but reading them by hand guesses at what is loaded instead of observing it.",
            "C": "Both engineers are on the same commit, so the checkout is not the variable.",
            "D": "Consolidation might mask the difference without ever revealing which layer caused it.",
        },
        "distractor_families": {
            "B": "right suspicion, indirect method",
            "C": "rules out a variable the scenario fixed",
            "D": "remedy before diagnosis",
        },
        "why": "Observe which configuration layers loaded before theorizing about which one differs.",
    },
    36: {
        "domain": "D1",
        "task": "1.6",
        "guide_anchor": "1.6 Skills in: splitting large code reviews into per-file local analysis passes plus a separate cross-file integration pass to avoid attention dilution",
        "stem": (
            "A review across 40 changed files produces findings that contradict one another and "
            "misses issues in the middle of the set. The review criteria themselves have been "
            "validated on smaller changes. How should the review be decomposed?"
        ),
        "options": {
            "A": "Run the same review once more against a more capable model tier.",
            "B": "Review only the files carrying the largest diffs in the change set.",
            "C": "Ask the model to re-read the full set before it states conclusions.",
            "D": "Run per-file local passes plus one separate cross-file integration pass.",
        },
        "key": ["D"],
        "explanations": {
            "A": "Attention dilutes across 40 files regardless of tier, and the criteria are already known to work at smaller scale.",
            "B": "Diff size is a poor proxy for risk, and the approach abandons coverage rather than restoring it.",
            "C": "A second read of the same oversized input reproduces the same middle-of-the-set gap.",
            "D": "Local issues get a focused pass per file, and the interactions that produce contradictions get a pass of their own.",
        },
        "distractor_families": {
            "A": "irrelevant lever",
            "B": "sampling presented as coverage",
            "C": "repeats the failing approach",
        },
        "why": "Split by concern: local findings per file, interactions in their own pass.",
    },
    37: {
        "domain": "D1",
        "task": "1.1",
        "guide_anchor": "1.1 Skills in: avoiding anti-patterns such as parsing natural language signals to determine loop termination",
        "negative": True,
        "stem": "Which of these does not describe how the agentic loop operates?",
        "options": {
            "A": "It continues on `tool_use` and terminates when `end_turn` is returned.",
            "B": "Tool results are appended to the history sent with the next request.",
            "C": "The program reads the assistant's text to judge whether work is done.",
            "D": "The model decides at each step whether to call a tool or to answer.",
        },
        "key": ["C"],
        "explanations": {
            "A": "This is the loop's control flow exactly as specified.",
            "B": "Appending results is what lets the model reason about what it has already learned.",
            "C": "Reading natural language to infer completion is the named anti-pattern; the signal is structural, not textual.",
            "D": "Model-driven decision making at each step is what separates an agentic loop from a fixed sequence.",
        },
        "distractor_families": {
            "A": "correct behavior offered as if wrong",
            "B": "correct behavior offered as if wrong",
            "D": "correct behavior offered as if wrong",
        },
        "why": "The loop reads `stop_reason`, never the prose.",
    },
    38: {
        "domain": "D1",
        "task": "1.5",
        "guide_anchor": "1.5 Skills in: implementing tool call interception hooks that block policy-violating actions and redirect to alternative workflows; choosing hooks over prompt-based enforcement when business rules require guaranteed compliance",
        "stem": (
            "Policy states that deletions above a threshold must never execute without a recorded "
            "approval. Deletions can be requested at any point in a session, and the current "
            "prompt-based rule is followed in the large majority of cases. Which mechanism "
            "enforces this?"
        ),
        "options": {
            "A": "A `PreToolUse` hook that blocks the call and routes it to approval.",
            "B": "A `PostToolUse` hook that records the approval once deletion completes.",
            "C": "`tool_choice` forcing the approval tool on the turn after the request.",
            "D": "A system prompt rule stating the threshold, plus two worked examples.",
        },
        "key": ["A"],
        "explanations": {
            "A": "Intercepting before execution is the only point at which the deletion can still be prevented rather than merely noted.",
            "B": "A post-execution hook produces an audit trail of deletions that already happened, which is not what never-without-approval means.",
            "C": "Forcing a tool shapes what the model calls next; it does not stop a call the model has already decided to make.",
            "D": "Examples raise compliance and leave a residual failure rate, which a policy written as never does not tolerate.",
        },
        "distractor_families": {
            "B": "right mechanism, too late",
            "C": "shapes selection, does not block",
            "D": "prompt where a mechanism is required",
        },
        "why": "Never means the action has to be impossible, not merely discouraged.",
    },
    39: {
        "domain": "D1",
        "task": "1.3",
        "guide_anchor": "1.3 Knowledge of: the AgentDefinition configuration including descriptions, system prompts, and tool restrictions; that subagent context must be explicitly provided in the prompt",
        "select_instruction": "Select two",
        "stem": "Which two statements are correct about subagent configuration?",
        "options": {
            "A": "A subagent inherits the coordinator's conversation history automatically.",
            "B": "A coordinator can spawn subagents only if `Task` is among its tools.",
            "C": "A subagent's system prompt is inherited unless it is explicitly set.",
            "D": "The allowed tools list restricts which tools the subagent may call.",
        },
        "key": ["B", "D"],
        "multi_answer": True,
        "explanations": {
            "A": "Subagent context is isolated, which is why anything it must know has to be written into its prompt.",
            "B": "Without `Task` the coordinator can reason about delegating and never actually delegate.",
            "C": "Each subagent definition carries its own system prompt; there is no inheritance to fall back on.",
            "D": "Tool restriction per subagent is what keeps each one inside its specialization.",
        },
        "distractor_families": {
            "A": "invented inheritance",
            "C": "invented inheritance",
        },
        "why": "Subagents inherit nothing: prompt, context, and tools are all declared per definition.",
    },
    40: {
        "domain": "D1",
        "task": "1.7",
        "guide_anchor": "1.7 Skills in: using fork_session to create parallel exploration branches (e.g., comparing two testing strategies or refactoring approaches from a shared codebase analysis)",
        "stem": (
            "You want to compare two refactoring approaches that both start from the same "
            "completed codebase analysis, and you expect to revisit both branches later. What "
            "fits?"
        ),
        "options": {
            "A": "Fork the session so each approach branches from the shared baseline.",
            "B": "Resume the analysis session twice in succession by its session name.",
            "C": "Start two fresh sessions, injecting the analysis summary into each.",
            "D": "Continue the most recent session once the first approach is finished.",
        },
        "key": ["A"],
        "explanations": {
            "A": "Forking gives two independent branches that share the analysis without either overwriting the other.",
            "B": "Resuming the same session twice extends one line of work; the second run inherits whatever the first one did.",
            "C": "Fresh sessions with an injected summary do isolate the branches, at the cost of re-deriving context the baseline already holds in full.",
            "D": "Continuing serializes the comparison and lets the first approach's context shape the second.",
        },
        "distractor_families": {
            "B": "same session, not a branch",
            "C": "two-valid-one-superior: isolation at the price of the baseline",
            "D": "serializes what should diverge",
        },
        "why": "Divergent branches from one baseline is what forking is for.",
    },
}
