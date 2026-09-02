"""Refinement pass: even out named artifacts across options.

The blind solver found that options naming a concrete artifact in backticks were
disproportionately the key, which is a shortcut a reader can exploit without
understanding the item. Naming artifacts in the distractors too removes the
signal and makes the distractors more specific, which is the same edit twice.

Two invented-artifact distractors are restored here. A plausible flag that does
not exist is a legitimate distractor, and it is only a problem when it is keyed.
"""

PATCH = {
    11: {
        "options": {
            "A": "In a skill under `.claude/skills/` described as covering migrations.",
            "B": "In the project `CLAUDE.md`, under a clearly marked migrations heading.",
            "C": "In a rules file with a `paths` glob that matches `migrations/`.",
            "D": "In a `.claude/commands/` command run before touching a migration.",
        },
        "key": ["C"],
    },
    23: {
        "options": {
            "A": "Build one composite search tool that runs the four searches internally.",
            "B": "Have the first subagent emit `Task` calls for the other three beneath it.",
            "C": "Emit the four `Task` calls within a single coordinator response.",
            "D": "Keep the sequence and narrow each subagent's scope to shorten it.",
        },
        "key": ["C"],
    },
    27: {
        "options": {
            "A": "Give it the full `web_search` tool set the research subagents use.",
            "B": "Give it a scoped `verify_fact` tool and route contradictions upward.",
            "C": "Keep its tool set as it is and have the coordinator verify each figure.",
            "D": "Move verification into the report step that runs after synthesis.",
        },
        "key": ["B"],
    },
    28: {
        "options": {
            "A": "Return `isError: false` for the authorization failure, since nothing came back.",
            "B": "Report the zero-match source as a valid empty result rather than an error.",
            "C": "Return `isError` with a category, a retryable flag, and a readable cause.",
            "D": "Return a uniform `source unavailable` status so all failures look alike.",
        },
        "key": ["B", "C"],
    },
    31: {
        "options": {
            "A": "Grep for `describe(` and `it(`, collecting every file that matches.",
            "B": "Glob for `**/*.test.tsx` and `**/*.spec.tsx`, then merge the two.",
            "C": "Grep for imports of the shared helpers and collect those files.",
            "D": "Glob for `**/*.tsx` and read each file to decide what it is.",
        },
        "key": ["B"],
    },
    39: {
        "options": {
            "A": "The `allowedTools` list restricts which tools the subagent may call.",
            "B": "A subagent inherits the coordinator's conversation history automatically.",
            "C": "A subagent's `systemPrompt` is inherited unless it is explicitly set.",
            "D": "A coordinator can spawn subagents only if `Task` is among its tools.",
        },
        "key": ["A", "D"],
    },
    41: {
        "options": {
            "A": "Set `CLAUDE_HEADLESS=1` and parse the job's standard output.",
            "B": "Run with `--batch` and read the aggregated results file it writes.",
            "C": "Run with `-p`, `--output-format json`, and `--json-schema`.",
            "D": "Run interactively in the container and capture the terminal output.",
        },
        "key": ["C"],
        "explanations": {
            "A": "There is no such environment variable, and parsing free-form output is what structured output exists to replace.",
            "B": "There is no `--batch` flag on the CLI; batching is a property of the API, not of a Claude Code invocation.",
            "C": "Non-interactive mode prevents the hang, and the two output flags together produce findings a later step can post without parsing prose.",
            "D": "Running interactively in CI is what hangs the job waiting for input that never arrives.",
        },
    },
    58: {
        "options": {
            "A": "Split the coming run into five batches so that failures stay contained.",
            "B": "Refine the prompt on a sample set before the 50,000-document run.",
            "C": "Resubmit the full batch with chunking applied to every document.",
            "D": "Resubmit only the failures, keyed by `custom_id`, once chunked.",
        },
        "key": ["B", "D"],
    },
}
