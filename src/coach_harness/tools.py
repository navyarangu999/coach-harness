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

def edit_file(path: str, old_text: str, new_text: str) -> str:
    """Replace one exact occurrence of old_text with new_text in a file."""
    content = Path(path).read_text(encoding="utf-8")

    count = content.count(old_text)
    if count == 0:
        return f"ERROR: old_text not found in {path}. No changes made."
    if count > 1:
        return (
            f"ERROR: old_text appears {count} times in {path}. "
            "Add more surrounding context to make it unique. No changes made."
        )

    Path(path).write_text(content.replace(old_text, new_text), encoding="utf-8")
    return f"edited {path}"