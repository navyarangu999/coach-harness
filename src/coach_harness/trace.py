"""Records what happened in one agent run and saves it to a JSON file."""
import json
from datetime import datetime
from pathlib import Path

# Claude Sonnet 5 pricing, USD per million tokens.
INPUT_COST_PER_MTOK = 2.0
OUTPUT_COST_PER_MTOK = 10.0

TRACES_DIR = Path("traces")


class Trace:
    def __init__(self, task: str, model: str):
        self.task = task
        self.model = model
        self.started_at = datetime.now().isoformat(timespec="seconds")
        self.steps: list[dict] = []
        self.input_tokens = 0
        self.output_tokens = 0
        self.outcome = "incomplete"

    def add_tokens(self, input_tokens: int, output_tokens: int) -> None:
        self.input_tokens += input_tokens
        self.output_tokens += output_tokens

    def add_tool_call(self, step: int, name: str, tool_input: dict, output: str) -> None:
        self.steps.append({
            "step": step,
            "tool": name,
            "input": tool_input,
            "output": output[:2000],  # keep traces readable
        })

    def cost_usd(self) -> float:
        return (
            self.input_tokens / 1_000_000 * INPUT_COST_PER_MTOK
            + self.output_tokens / 1_000_000 * OUTPUT_COST_PER_MTOK
        )

    def save(self) -> Path:
        TRACES_DIR.mkdir(exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = TRACES_DIR / f"trace_{stamp}.json"
        data = {
            "task": self.task,
            "model": self.model,
            "started_at": self.started_at,
            "outcome": self.outcome,
            "num_steps": len(self.steps),
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "cost_usd": round(self.cost_usd(), 6),
            "steps": self.steps,
        }
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return path