"""Scenario 2 rewrite: Code Generation with Claude Code (items 11-20)."""

PATCH = {
    11: {
        "domain": "D3",
        "task": "3.3",
        "guide_anchor": "3.3 Skills in: creating .claude/rules/ files with YAML frontmatter path scoping so rules load only when editing matching files",
        "stem": (
            "Conventions for database migrations apply only when someone edits files under "
            "`migrations/`. They must load without anyone invoking them, and they should not "
            "occupy context when the work is elsewhere. Where do they belong?"
        ),
        "options": {
            "A": "In a skill whose description states that it covers migration work.",
            "B": "In the project `CLAUDE.md`, under a clearly marked migrations heading.",
            "C": "In a rules file with a `paths` glob that matches `migrations/`.",
            "D": "In a slash command engineers run before touching any migration.",
        },
        "key": ["C"],
        "explanations": {
            "A": "A skill is invoked on demand. Its description makes it findable, not automatic, so the conventions load only when someone thinks to ask.",
            "B": "`CLAUDE.md` is always loaded, so the conventions would occupy context during every unrelated task.",
            "C": "Path-scoped rules load automatically and only when a matching file is being edited, which is both requirements at once.",
            "D": "A command depends on the engineer remembering to run it, which is the automatic loading the scenario rules out.",
        },
        "distractor_families": {
            "A": "on-demand where automatic is required",
            "B": "always-loaded where conditional is required",
            "D": "depends on human recall",
        },
        "why": "Automatic plus conditional is exactly what a path glob buys you.",
    },
    12: {
        "domain": "D3",
        "task": "3.2",
        "guide_anchor": "3.2 Skills in: choosing between skills (on-demand invocation for task-specific workflows) and CLAUDE.md (always-loaded universal standards)",
        "stem": (
            "The team has a nine-step release procedure run about twice a month, and a file naming "
            "convention that applies to every file in the repository. Both are currently pasted "
            "into chat by hand. How should they be handled?"
        ),
        "options": {
            "A": "The release procedure as a skill, the naming convention in `CLAUDE.md`.",
            "B": "Both as skills, so that neither one loads until it becomes relevant.",
            "C": "The release procedure in `CLAUDE.md`, the naming convention as a rule.",
            "D": "The release procedure as a command, the naming convention as a skill.",
        },
        "key": ["A"],
        "explanations": {
            "A": "A long procedure needed twice a month is on-demand work; a convention that governs every file is a universal standard that should always be loaded.",
            "B": "Making the naming convention on-demand means it is absent from the many edits where nobody thinks to invoke it.",
            "C": "This inverts both: a nine-step procedure occupies context permanently while a repository-wide rule loads only for some paths.",
            "D": "A command is a reasonable home for a procedure, but putting a universal convention behind on-demand invocation repeats the error in B.",
        },
        "distractor_families": {
            "B": "on-demand where always-loaded is required",
            "C": "both halves inverted",
            "D": "half right, universal standard still gated",
        },
        "why": "Frequency and scope decide the home: universal and always, or specific and on demand.",
    },
    13: {
        "domain": "D3",
        "task": "3.1",
        "guide_anchor": "3.1 Knowledge of: the CLAUDE.md configuration hierarchy: user-level (~/.claude/CLAUDE.md), project-level, and directory-level; user-level settings are not shared with teammates via version control",
        "stem": (
            "An engineer wants her personal preferences applied in every repository she works in, "
            "while the team's conventions must reach everyone who clones this one. Which pair is "
            "correct?"
        ),
        "options": {
            "A": "`~/.claude/config.json` for hers, the repository `CLAUDE.md` for the team.",
            "B": "`.claude/settings.yaml` for hers, the `.claude/rules/` directory for the team.",
            "C": "The repository `CLAUDE.md` for both, with hers in a clearly marked section.",
            "D": "`~/.claude/CLAUDE.md` for hers, the repository `CLAUDE.md` for the team.",
        },
        "key": ["D"],
        "explanations": {
            "A": "The project half is right, but instructions for Claude live in `CLAUDE.md`; there is no `config.json` in this hierarchy.",
            "B": "`.claude/rules/` is a real home for team conventions, but a settings file is not where personal instructions go, and this pair puts hers inside the repository.",
            "C": "Anything committed to the repository reaches everyone who clones it, so her preferences would be imposed on the team.",
            "D": "User-level configuration follows the person across every repository and is never shared; project-level travels with the clone.",
        },
        "distractor_families": {
            "A": "invented artifact",
            "B": "invented artifact, half-plausible pairing",
            "C": "scope collision: personal settings shared with the team",
        },
        "why": "The axis is who receives it: the user everywhere, or everyone who clones this repository.",
    },
    14: {
        "domain": "D3",
        "task": "3.4",
        "guide_anchor": "3.4 Skills in: selecting direct execution for well-understood changes with clear scope (e.g., a single-file bug fix with a clear stack trace)",
        "stem": (
            "A developer asks for a fix to a null dereference in one utility function. She has the "
            "stack trace and the failing input, and the function has no other callers under "
            "change. What is the best first step?"
        ),
        "options": {
            "A": "Enter plan mode so the change is scoped before any edit is made.",
            "B": "Make the fix directly and review the resulting diff with her.",
            "C": "Write a failing test first and iterate on it until it passes.",
            "D": "Explore the function's call sites before changing anything at all.",
        },
        "key": ["B"],
        "explanations": {
            "A": "Plan mode earns its cost on architectural decisions and multi-file work; here the scope is one function and the cause is already known.",
            "B": "A single-file fix with a known cause and a known failing input is the textbook case for direct execution.",
            "C": "Test-driven iteration is valuable when behavior is unclear, but the failing input is already in hand and the fix is one line of judgment.",
            "D": "Call-site exploration matters when a signature changes; the scenario states the callers are not in scope.",
        },
        "distractor_families": {
            "A": "over-ceremony for a scoped change",
            "C": "good practice, wrong trigger",
            "D": "investigation the scenario already closed",
        },
        "why": "Plan mode is for choosing among approaches, not for changes with one obvious shape.",
    },
    15: {
        "domain": "D3",
        "task": "3.5",
        "guide_anchor": "3.5 Skills in: using the interview pattern to surface design considerations before implementing solutions in unfamiliar domains",
        "stem": (
            "A team is adding rate limiting to a service for the first time. Nobody has worked "
            "with it before, and when asked what behavior they want they are unsure what they "
            "even need to specify. Which approach fits best?"
        ),
        "options": {
            "A": "Supply input and output examples of limited and unlimited requests.",
            "B": "Enter plan mode so the design is reviewed before implementation.",
            "C": "Have the agent ask questions that surface what they have not considered.",
            "D": "Implement a first version directly and refine it once the gaps appear.",
        },
        "key": ["C"],
        "explanations": {
            "A": "Examples are the strongest tool when you know the transformation you want. This team cannot yet state it.",
            "B": "Plan mode produces a plan from the requirements you bring it, and the requirements are the missing piece.",
            "C": "The interview pattern surfaces the considerations a team new to a domain does not know to raise, which is precisely the stated gap.",
            "D": "Building first and discovering the requirements through rework is the cost the interview is meant to avoid.",
        },
        "distractor_families": {
            "B": "right technique, missing precondition",
            "A": "requires knowledge the team lacks",
            "D": "discovery by rework",
        },
        "why": "When the team cannot state the requirement, elicit it before designing to it.",
    },
    16: {
        "domain": "D5",
        "task": "5.4",
        "guide_anchor": "5.4 Skills in: having agents maintain scratchpad files recording key findings, referencing them for subsequent questions to counteract context degradation",
        "stem": (
            "Two hours into a refactor the agent begins citing patterns typical of such services "
            "rather than what is in this repository, and repeats work it already completed. The "
            "code it produced earlier in the session was correct. What should be done?"
        ),
        "options": {
            "A": "Move to a model configuration with a larger context window.",
            "B": "Clear the context and restart with what has been learned so far.",
            "C": "Persist the refactor state to a scratchpad and work from that file.",
            "D": "Summarize the session so far and continue in the same session.",
        },
        "key": ["C"],
        "explanations": {
            "A": "A larger window delays the same degradation without addressing where the findings live.",
            "B": "Clearing discards the specific discoveries that are the expensive part of the session.",
            "C": "A scratchpad moves the findings out of the window entirely, so they survive degradation and can be referenced deliberately.",
            "D": "An in-session summary is a reasonable step, but it leaves the record inside the same degrading context it is meant to protect.",
        },
        "distractor_families": {
            "A": "irrelevant lever",
            "B": "nuke and reset",
            "D": "right instinct, wrong storage",
        },
        "why": "Degradation is about where findings live, not how much room they have.",
    },
    17: {
        "domain": "D5",
        "task": "5.1",
        "guide_anchor": "5.1 Skills in: placing key findings summaries at the beginning of aggregated inputs and organizing detailed results with explicit section headers to mitigate position effects",
        "stem": (
            "A code review agent produces a long report. Reviewers act on the first and last "
            "sections and consistently miss issues in the middle, including severe ones. The "
            "findings themselves have been verified as accurate. What addresses this?"
        ),
        "options": {
            "A": "Drop findings below a severity threshold so the report is shorter.",
            "B": "Split the report into one comment attached to each affected file.",
            "C": "Append a summary at the end so that nothing goes unnoticed.",
            "D": "Lead with the key findings and add headers that make it navigable.",
        },
        "key": ["D"],
        "explanations": {
            "A": "Filtering by severity removes real findings to work around a position effect, and the missed issues include severe ones.",
            "B": "Per-file comments are a genuine improvement in delivery, but each one still has a middle that readers skim.",
            "C": "A trailing summary reinforces the end, which is already one of the two positions readers do attend to.",
            "D": "Front-loading what matters and giving the body explicit structure works with the way long inputs are read rather than against it.",
        },
        "distractor_families": {
            "A": "suppresses findings to hide the symptom",
            "B": "plausible delivery change, same failure inside",
            "C": "reinforces a position that already works",
        },
        "why": "Information in the middle gets lost, so put what matters where attention lands.",
    },
    18: {
        "domain": "D5",
        "task": "5.4",
        "guide_anchor": "5.4 Skills in: spawning subagents to investigate specific questions while the main agent preserves high-level coordination",
        "stem": (
            "You must assess whether a deprecation affects any of 11 packages, each around 80 "
            "files with its own conventions. The combined relevant code runs to several times "
            "your context window. Which approach fits?"
        ),
        "options": {
            "A": "Grep the symbol across all packages and read the lines around each hit.",
            "B": "Map each package from its imports before reading any implementation.",
            "C": "Read the three largest packages in depth and generalize from those.",
            "D": "Delegate one scoped subagent per package, each returning call sites.",
        },
        "key": ["D"],
        "explanations": {
            "A": "Grep finds the direct hits and misses every package that renames the symbol behind a wrapper, which is likely across 11 sets of conventions.",
            "B": "Structural mapping is the right opening move for understanding one unfamiliar package, but eleven maps still land in the same window.",
            "C": "Generalizing from three packages assumes the other eight follow their conventions, which the scenario explicitly denies.",
            "D": "Each subagent absorbs the exploration in its own context and returns a compact answer, so the coordinator holds only conclusions.",
        },
        "distractor_families": {
            "A": "misses aliasing across conventions",
            "B": "right technique, wrong scale",
            "C": "sampling presented as coverage",
        },
        "why": "When the material exceeds the window, delegate the reading and keep the conclusions.",
    },
    19: {
        "domain": "D5",
        "task": "5.1",
        "guide_anchor": "5.1 Skills in: trimming verbose tool outputs to only relevant fields before they accumulate in context; extracting transactional facts into a persistent block outside summarized history",
        "select_instruction": "Select two",
        "stem": (
            "A session is approaching its context limit. Tool outputs carry more than forty fields "
            "each, of which the agent uses four, and the conversation spans several topics that "
            "are already resolved. Which two actions are appropriate?"
        ),
        "options": {
            "A": "Switch to a model configuration with a larger context window.",
            "B": "Prune each tool output to the four fields the agent actually uses.",
            "C": "Start a new session so that the context is clean from this point.",
            "D": "Summarize the resolved topics, keeping the active thread verbatim.",
        },
        "key": ["B", "D"],
        "multi_answer": True,
        "explanations": {
            "A": "A larger window postpones the limit without reducing what is consuming it.",
            "B": "Thirty-six unused fields per call are pure accumulation, and trimming them is the cheapest reclamation available.",
            "C": "A clean session discards the resolved history along with the active thread that still needs it.",
            "D": "Compressing what is settled while preserving what is live is the shape progressive summarization is meant to take.",
        },
        "distractor_families": {
            "A": "irrelevant lever",
            "C": "nuke and reset",
        },
        "why": "Reclaim context by removing what is unused and compressing what is finished.",
    },
    20: {
        "domain": "D5",
        "task": "5.4",
        "guide_anchor": "5.4 Skills in: summarizing key findings from one exploration phase before spawning sub-agents for the next phase, injecting summaries into initial context",
        "negative": True,
        "stem": (
            "Which of these is not an appropriate response to a session approaching its context "
            "limit?"
        ),
        "options": {
            "A": "Summarizing the portions of the conversation that are already resolved.",
            "B": "Pruning verbose tool outputs down to the fields the agent actually uses.",
            "C": "Persisting the working state externally and continuing from that file.",
            "D": "Clearing the context and starting over without carrying a summary.",
        },
        "key": ["D"],
        "explanations": {
            "A": "Compressing settled material is the standard way to reclaim room without losing the thread.",
            "B": "Field pruning removes accumulation that was never contributing to the reasoning.",
            "C": "Externalizing state is what allows work to cross a context boundary intact.",
            "D": "Starting over with nothing carried forward throws away the findings the session was assembling, which is the cost the other three avoid.",
        },
        "distractor_families": {
            "A": "valid technique offered as if wrong",
            "B": "valid technique offered as if wrong",
            "C": "valid technique offered as if wrong",
        },
        "why": "Every remedy here preserves the findings except the one that discards them.",
    },
}
