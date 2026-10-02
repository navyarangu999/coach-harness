# coach-harness

A coding agent built from scratch on the Claude API — it reads a codebase, edits files, runs tests, and iterates until the task is done. No agent framework; the loop, the tools, the safety controls, and the evaluation are all hand-built to show how a coding agent actually works under the hood.

The headline is not "it calls an LLM." It's that every run is **measured**: the project ships with a self-checking benchmark that runs the agent over a set of buggy tasks and reports a real pass rate, with cost and time per task.

## Result

Benchmarked on 10 single-bug Python tasks spanning common error categories (off-by-one, wrong operator, mutable default argument, integer division, slicing, conditional ordering, string-method misuse, accumulator init, whitespace handling, recursive base case).

| Metric | Value |
| --- | --- |
| Pass rate | **10 / 10 (100%)** |
| Model | `claude-sonnet-5` |
| Avg. time per fix | ~14 s |
| Avg. cost per fix | a few cents |

Pass/fail is judged by the harness **independently re-running pytest** after the agent finishes — never by the agent's own claim that it succeeded.

## How it works

```
task ─▶ ask model (task + available tools)
          │
          ▼
   model replies ──▶ final answer?  ──▶ done
          │                 ▲
          ▼                 │
   model requests a tool    │
          │                 │
          ▼                 │
   harness runs the tool    │
   (read / write / edit /   │
    run_shell) and feeds    │
   the result back ─────────┘
          (repeat up to MAX_STEPS)
```

The agent is given a task and a set of tools. On each step the model either returns a final answer or asks to use a tool; the harness runs the tool, feeds the result back, and loops until the model is done or a step limit is hit.

### Tools

| Tool | Purpose |
| --- | --- |
| `read_file` | Read a text file |
| `write_file` | Create or overwrite a file |
| `edit_file` | Replace one **unique** occurrence of a string (preferred for edits) |
| `run_shell` | Run a shell command, with a timeout |

`edit_file` refuses to act unless the target text matches exactly once — if it's missing or ambiguous it returns an error telling the model to add more context, so a blind replace can never corrupt a file.

### Instrumentation

Every run is saved to `traces/` as a JSON file recording the task, every tool call, step count, token usage, cost, and outcome. These traces are the raw data behind the benchmark.

## Project layout

```
src/coach_harness/
  agent.py      # the agent loop + tool schemas
  tools.py      # tool implementations
  trace.py      # per-run recording + cost calculation
  evaluate.py   # runs the agent over every task in tasks/ and scores it
tasks/          # buggy practice tasks (code + failing tests)
traces/         # saved run records (git-ignored)
```

## Setup

Requires Python 3.11+ and an Anthropic API key.

```bash
# install dependencies (uses uv)
python -m pip install uv
python -m uv sync

# add your key
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
```

## Usage

Run the agent on a single task:

```bash
python -m uv run python -m coach_harness.agent "fix the failing tests in tasks/countdown"
```

Run the full benchmark and print the results table:

```bash
python -m uv run python -m coach_harness.evaluate
```

## Design decisions

- **No agent framework.** The loop is written by hand against the raw API. The point of the project is to understand agent mechanics, not hide them behind LangChain or similar.
- **Independent verification.** The evaluator re-runs the tests itself rather than trusting the agent's self-report. A benchmark the agent can grade for itself isn't a benchmark.
- **Tasks must start red.** The evaluator skips any task whose tests already pass, so the score only ever reflects bugs that were genuinely fixed.
- **Safe edits by construction.** `edit_file` requires a unique match, making targeted edits predictable instead of rewriting whole files.
- **Hard limits.** A step cap and a shell timeout keep a misbehaving run from looping forever or running up cost.

## Limitations & next steps

- Tasks are currently single-file, single-bug. Multi-file and multi-bug tasks would stress the agent harder and make the pass rate more discriminating.
- Shell commands run on the host; a Docker sandbox would isolate them.
- No context-compaction strategy yet for very long runs (tool output is truncated crudely).
- Planned: an ablation study (e.g. removing the "verify with tests" instruction) to measure how much each design choice contributes to the pass rate.

---

Built as a portfolio project to demonstrate agent design, tool use, and rigorous evaluation.