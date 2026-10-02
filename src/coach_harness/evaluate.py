"""Runs the agent over every task in tasks/ and reports a results table."""
import io
import subprocess
import sys
import time
from contextlib import redirect_stdout
from pathlib import Path

from .agent import run_agent, MODEL

TASKS_DIR = Path("tasks")


def run_pytest(task_dir: Path) -> bool:
    """Return True if all tests in task_dir pass."""
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=task_dir,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def evaluate_task(task_dir: Path) -> dict:
    name = task_dir.name

    # 1. Confirm the task starts in a failing state.
    if run_pytest(task_dir):
        return {"task": name, "status": "SKIPPED (already passing)"}

    # 2. Run the agent on the task. Capture its console output so the table
    #    stays clean; the trace file still records everything.
    task = (
        f"The tests in the {task_dir.as_posix()} folder are failing. "
        "Read the code, find the bug, fix it, and run the tests to confirm "
        "they all pass."
    )
    start = time.time()
    captured = io.StringIO()
    with redirect_stdout(captured):
        run_agent(task)
    elapsed = time.time() - start

    # 3. Independently check the real outcome.
    passed = run_pytest(task_dir)

    return {
        "task": name,
        "status": "PASS" if passed else "FAIL",
        "seconds": round(elapsed, 1),
    }


def main() -> None:
    task_dirs = sorted(p for p in TASKS_DIR.iterdir() if p.is_dir())
    if not task_dirs:
        print("No task folders found in tasks/")
        return

    print(f"Evaluating {len(task_dirs)} task(s) with {MODEL}...\n")
    results = []
    for task_dir in task_dirs:
        print(f"-> {task_dir.name} ...", end=" ", flush=True)
        result = evaluate_task(task_dir)
        results.append(result)
        print(result["status"])

    # Summary table
    print("\n=== Results ===")
    print(f"{'task':<20} {'status':<10} {'seconds':>8}")
    print("-" * 40)
    passes = 0
    for r in results:
        secs = r.get("seconds", "-")
        print(f"{r['task']:<20} {r['status']:<10} {str(secs):>8}")
        if r["status"] == "PASS":
            passes += 1

    scored = [r for r in results if r["status"] in ("PASS", "FAIL")]
    if scored:
        rate = passes / len(scored) * 100
        print("-" * 40)
        print(f"Pass rate: {passes}/{len(scored)} ({rate:.0f}%)")


if __name__ == "__main__":
    main()