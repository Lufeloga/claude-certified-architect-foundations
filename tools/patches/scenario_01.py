"""Scenario 1 rewrite: Customer Support Resolution Agent (items 1-10).

Every option is rebuilt to the same register and a comparable length, so option
length carries no signal. Distractors gain real specificity rather than padding:
a concrete wrong answer is a better distractor than a vague one, which raises
difficulty and removes the length tell in the same edit.
"""

PATCH = {
    1: {
        "domain": "D1",
        "task": "1.1",
        "guide_anchor": "1.1 Skills in: avoiding anti-patterns such as checking for assistant text content as a completion indicator",
        "stem": (
            "The agent sometimes stops mid-task, closing the conversation with a line like "
            '"I\'ll look that up now." Every tool the agent called returned successfully, and the '
            "loop exits as soon as the model produces text. What is the flaw?"
        ),
        "options": {
            "A": "End the loop on `end_turn` rather than on the presence of assistant text.",
            "B": "Raise `maxTurns`, which is capping the loop before the task can finish.",
            "C": "Instruct the model to complete all tool work before producing narration.",
            "D": "Append each tool result to the history so the model tracks what it did.",
        },
        "key": ["A"],
        "explanations": {
            "A": "The stop signal is structural, and a single turn can carry both text and a `tool_use` block. Treating text as completion truncates work the model intended to continue.",
            "B": "An iteration cap is a safety fuse, never the primary stopping mechanism; the loop here is ending early by design, not by exhaustion.",
            "C": "Prose cannot repair a mechanical termination condition that fires before the model is consulted again.",
            "D": "Dropping tool results produces an agent that loses track of its work, not one that halts while announcing an intention.",
        },
        "distractor_families": {
            "B": "wrong level: configuration knob for a control-flow defect",
            "C": "prompt where a mechanism is required",
            "D": "real anti-pattern, wrong symptom",
        },
        "why": "The loop terminates on `stop_reason`, and text and a tool call can arrive together.",
    },
    2: {
        "domain": "D1",
        "task": "1.4",
        "guide_anchor": "1.4 Skills in: implementing programmatic prerequisites that block downstream tool calls until prerequisite steps have completed",
        "stem": (
            "Policy requires identity verification with `get_customer` before any refund executes. "
            "The system prompt states this explicitly and was reviewed for clarity, and 3% of "
            "transcripts still show `process_refund` running first. What should be done?"
        ),
        "options": {
            "A": "Add explicit ordering language and two worked examples to the system prompt.",
            "B": "Block `process_refund` programmatically until `get_customer` returns an id.",
            "C": "Force `get_customer` with `tool_choice` on every request in the conversation.",
            "D": "Route refunds to a subagent invoked only after verification has completed.",
        },
        "key": ["B"],
        "explanations": {
            "A": "This is the mechanism that already failed. Prompt instructions retain a non-zero failure rate, and the 3% is that rate.",
            "B": "A prerequisite gate makes the out-of-order call structurally impossible rather than merely discouraged.",
            "C": "Forcing the tool on every request is the right mechanism at the wrong scope: the agent could never return a final answer.",
            "D": "Moving the call into a subagent relocates the work without gating it; nothing prevents the subagent from being invoked early.",
        },
        "distractor_families": {
            "A": "prompt where a mechanism is required",
            "C": "right mechanism, wrong scope",
            "D": "restructuring that leaves the guarantee unenforced",
        },
        "why": "When compliance must be deterministic, a request is not a guarantee.",
    },
    3: {
        "domain": "D1",
        "task": "1.4",
        "guide_anchor": "1.4 Skills in: compiling structured handoff summaries (customer ID, root cause, refund amount, recommended action) when escalating to human agents who lack access to the conversation transcript",
        "stem": (
            "The agent escalates mid-process to a human specialist who works from a separate queue "
            "and has no access to the conversation transcript. What should the handoff contain?"
        ),
        "options": {
            "A": "The full transcript, so the specialist can form an independent judgment.",
            "B": "The last three messages plus a read on the customer's current tone.",
            "C": "A session link the specialist can open to review the case directly.",
            "D": "Customer id, root cause, refund amount, and the recommended action.",
        },
        "key": ["D"],
        "explanations": {
            "A": "Handing over raw material transfers the reading work rather than the conclusion, and the specialist has to redo the diagnosis.",
            "B": "Three messages are a fragment of the case, and tone is not a fact the specialist can act on.",
            "C": "The scenario states the specialist has no transcript access, so a link resolves to nothing.",
            "D": "A self-contained package gives the specialist identity, cause, amount at stake, and a proposed action, which is everything needed to act.",
        },
        "distractor_families": {
            "A": "unprocessed dump",
            "B": "false proxy: sentiment in place of case facts",
            "C": "assumes access the scenario denies",
        },
        "why": "A handoff is a decision package, not a pointer to where the decision could be reconstructed.",
    },
    4: {
        "domain": "D1",
        "task": "1.5",
        "guide_anchor": "1.5 Skills in: implementing PostToolUse hooks to normalize heterogeneous data formats (Unix timestamps, ISO 8601, numeric status codes) from different MCP tools before the agent processes them",
        "stem": (
            "Three MCP tools return order status as a Unix timestamp, an ISO 8601 string, and a "
            "numeric code respectively. All three tools are healthy and their outputs are correct. "
            "The agent's reasoning about which event came first is inconsistent. Where does "
            "normalization belong?"
        ),
        "options": {
            "A": "In each tool's description, documenting the timestamp format it returns.",
            "B": "In the system prompt, as an explicit rule for comparing the three formats.",
            "C": "In a `PreToolUse` hook that rewrites each request before it is dispatched.",
            "D": "In a `PostToolUse` hook, before the model reasons over the returned values.",
        },
        "key": ["D"],
        "explanations": {
            "A": "Documenting the inconsistency leaves the model to reconcile it on every comparison instead of removing the variance.",
            "B": "A prompt rule asks the model to do conversion work reliably on every turn, which is precisely what it is failing to do.",
            "C": "A pre-call hook intercepts the outgoing request; the heterogeneity is in what comes back.",
            "D": "Results are transformed once, in code, before they enter the model's reasoning at all.",
        },
        "distractor_families": {
            "A": "documents the problem instead of resolving it",
            "B": "prompt where a mechanism is required",
            "C": "right mechanism, wrong direction",
        },
        "why": "Normalize where the variance enters, not where the model has to cope with it.",
    },
    5: {
        "domain": "D1",
        "task": "1.3",
        "guide_anchor": "1.3 Knowledge of: that subagent context must be explicitly provided in the prompt, subagents do not automatically inherit parent context",
        "stem": (
            "A specialist subagent receives a prompt naming its task and the customer id. It "
            "completes every task it is given without error, yet its resolutions repeatedly "
            "violate constraints the customer stated earlier in the conversation. What explains "
            "this?"
        ),
        "options": {
            "A": "Subagent context is isolated, so constraints must be restated in its prompt.",
            "B": "The coordinator lacks `Task` in `allowedTools`, so the delegation is partial.",
            "C": "The coordinator's context degraded before it composed the delegation prompt.",
            "D": "Subagents retain parent memory only for the turn in which they are spawned.",
        },
        "key": ["A"],
        "explanations": {
            "A": "A subagent sees its prompt and nothing else. A constraint stated to the coordinator never reaches it unless it is written into the delegation.",
            "B": "Without `Task` the coordinator could not spawn the subagent at all; here the subagent runs and completes work.",
            "C": "Degradation would produce erratic delegations across the board, not the consistent omission of one class of information.",
            "D": "There is no partial inheritance window. Subagents do not inherit parent memory at any point.",
        },
        "distractor_families": {
            "B": "real requirement, contradicted by the stated symptom",
            "C": "plausible cause, wrong failure signature",
            "D": "invented mechanism",
        },
        "why": "Isolation is total, so anything the subagent must honor has to be handed to it.",
    },
    6: {
        "domain": "D1",
        "task": "1.7",
        "guide_anchor": "1.7 Skills in: choosing between session resumption (when prior context is mostly valid) and starting fresh with injected summaries (when prior tool results are stale)",
        "stem": (
            "You return to an investigation session paused five days ago. Of its 26 cached tool "
            "results, 24 are order statuses that have since changed. The reasoning the session "
            "recorded about the customer's entitlement is unaffected by those changes. What do "
            "you do?"
        ),
        "options": {
            "A": "Resume the session and flag in each response that statuses may be stale.",
            "B": "Start fresh, inject a summary of the reasoning, and re-fetch the statuses.",
            "C": "Resume the session and selectively re-fetch the 24 statuses that changed.",
            "D": "Fork the session so both the old and the new investigation stay available.",
        },
        "key": ["B"],
        "explanations": {
            "A": "A caveat does not stop the model from reasoning over the stale values that are still sitting in context.",
            "B": "When the great majority of tool results are stale, the reliable move is a clean session carrying forward only the part that survived, which is the reasoning.",
            "C": "Targeted re-fetch is the right call when most of the context still holds. Here 24 of 26 results are invalid, so the session is stale rather than lightly outdated.",
            "D": "Forking preserves a baseline for divergent exploration, which is not the problem: there is one line of investigation and its data expired.",
        },
        "distractor_families": {
            "A": "band-aid that leaves the bad data in place",
            "C": "correct technique, wrong threshold",
            "D": "right tool for a different question",
        },
        "why": "Resume when context is mostly valid; restart with a summary when it mostly is not.",
    },
    7: {
        "domain": "D2",
        "task": "2.3",
        "guide_anchor": '2.3 Knowledge of: tool_choice configuration options: "auto", "any", and forced tool selection',
        "select_instruction": "Select two",
        "stem": "Which two statements correctly describe `tool_choice`?",
        "options": {
            "A": "Setting `auto` guarantees the model calls at least one tool per turn.",
            "B": "Setting `any` forces a tool call but lets the model choose which one.",
            "C": "A forced tool selection persists for the remainder of the conversation.",
            "D": "Forcing one tool on every request prevents a final text answer.",
        },
        "key": ["B", "D"],
        "multi_answer": True,
        "explanations": {
            "A": "`auto` leaves the model free to answer in text without calling anything; that is exactly what distinguishes it from `any`.",
            "B": "`any` guarantees a call is made while leaving selection to the model.",
            "C": "`tool_choice` is set per request. Nothing carries it forward on its own.",
            "D": "If every request must call the named tool, the turn that would carry the final answer is consumed by another call.",
        },
        "distractor_families": {
            "A": "vocabulary inversion: the two settings swapped",
            "C": "invented persistence",
        },
        "why": "`any` guarantees a call; `auto` does not; and forcing is per request, not a mode.",
    },
    8: {
        "domain": "D2",
        "task": "2.4",
        "guide_anchor": "2.4 Knowledge of: MCP resources as a mechanism for exposing content catalogs to reduce exploratory tool calls",
        "stem": (
            "Before answering entitlement questions the agent calls `list_plans` to see what "
            "exists, then `get_plan` for the one it needs. `list_plans` runs in nearly every "
            "conversation and the catalog changes twice a year. An engineer proposes caching its "
            "response. What is the better approach?"
        ),
        "options": {
            "A": "Cache the response, since the catalog changes only twice a year.",
            "B": "Merge the two tools so a single call returns catalog and plan.",
            "C": "Expose the plan catalog as an MCP resource the agent can consult.",
            "D": "Sharpen the description so `list_plans` is called only when needed.",
        },
        "key": ["C"],
        "explanations": {
            "A": "Caching is defensible and would help, but it only makes an unnecessary call cheap. The call itself is what should disappear.",
            "B": "Merging couples a browse operation to a fetch operation and returns catalog data the agent usually does not need.",
            "C": "A resource gives the agent visibility into what exists without spending a tool call to ask.",
            "D": "The agent is not calling the tool by mistake; it calls it because it genuinely has no other way to see the catalog.",
        },
        "distractor_families": {
            "A": "optimizes the symptom",
            "B": "over-coupling",
            "D": "treats a visibility gap as a selection problem",
        },
        "why": "A resource makes the exploratory call unnecessary; a cache only makes it faster.",
    },
    9: {
        "domain": "D2",
        "task": "2.1",
        "guide_anchor": "2.1 Skills in: splitting generic tools into purpose-specific tools with defined input/output contracts",
        "stem": (
            "A `run_report` tool takes a free-text spec and returns a rendered table, a JSON "
            "object, or prose depending on what was asked. Its description is thorough and "
            "accurate, and the tool is selected correctly every time. Downstream consumers fail "
            "on 20% of calls. What is the correct fix?"
        ),
        "options": {
            "A": "Add an enum to the spec parameter listing the supported report types.",
            "B": "Split it into purpose-specific tools with declared return shapes.",
            "C": "Post-process the output into one shape before consumers receive it.",
            "D": "Rename it and document the varying return shape in the description.",
        },
        "key": ["B"],
        "explanations": {
            "A": "An enum constrains what goes in. What varies here is what comes out, so the consumers keep breaking.",
            "B": "Each report type becomes a tool with a typed parameter and a single declared return shape, which is a contract consumers can rely on.",
            "C": "A normalization layer hides the variance from consumers while leaving three shapes flowing through the system.",
            "D": "The description is already accurate and selection already works; documenting the variance does not remove it.",
        },
        "distractor_families": {
            "A": "constrains the input when the output is what varies",
            "C": "band-aid downstream",
            "D": "documents the problem instead of resolving it",
        },
        "why": "Varying input takes an enum; varying output takes separate tools.",
    },
    10: {
        "domain": "D5",
        "task": "5.2",
        "guide_anchor": "5.2 Knowledge of: why sentiment-based escalation and self-reported confidence scores are unreliable proxies for actual case complexity",
        "negative": True,
        "stem": "Which is the weakest basis for escalating a conversation to a human?",
        "options": {
            "A": "The customer has explicitly asked to speak with a person.",
            "B": "The request falls outside the agent's documented authority.",
            "C": "The agent reports low confidence in the answer it produced.",
            "D": "Three turns have passed with no progress on the issue.",
        },
        "key": ["C"],
        "explanations": {
            "A": "An explicit request for a human is the strongest trigger there is, and it is honored immediately.",
            "B": "Acting outside documented authority is exactly the boundary escalation exists to respect.",
            "C": "A self-reported score is the model grading its own work, and it correlates poorly with whether the case is actually beyond the agent.",
            "D": "Lack of progress is observable from the outside and does not depend on the model assessing itself.",
        },
        "distractor_families": {
            "A": "strongest trigger, offered as if weak",
            "B": "policy boundary, objectively checkable",
            "D": "objective progress signal",
        },
        "why": "Escalation triggers should be observable, not self-reported.",
    },
}
