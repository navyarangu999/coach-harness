"""Tools the agent can call. Each function does one thing and returns text."""
import subprocess
from pathlib import Path


def read_file(path: str) -> str:
    """Return the contents of a text file."""
    return Path(path).read_text(encoding="utf-8")


def write_file(path: str, content: str) -> str:
    """Create or overwrite a file with the given content."""
    Path(path).write_text(content, encoding="utf-8")
    return f"wrote {path}"


def run_shell(command: str) -> str:
    """Run a shell command and return its combined output."""
    result = subprocess.run(
        command, shell=True, capture_output=True, text=True, timeout=30
    )
    return (result.stdout + result.stderr) or "(no output)"