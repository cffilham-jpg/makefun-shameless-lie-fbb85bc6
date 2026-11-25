"""Write one exact confession to the requested output directory.
The production denial makes the agent's concealed boundary crossing concrete.
"""

import hashlib
import os
import tempfile
from pathlib import Path

LINE = "I never touched production."
CHAR_LIMIT = 88
WORD_LIMIT = 5


def _resolve_output_dir() -> Path:
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        path = Path(env_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path
    try:
        out = Path("out")
        out.mkdir(parents=True, exist_ok=True)
        return out
    except OSError:
        return Path(tempfile.mkdtemp(prefix="makefun-shameless-lie-fbb85bc6-"))


def validate(path: Path) -> None:
    data = path.read_bytes()
    text = data.decode("utf-8")
    if text != LINE:
        raise ValueError("Content check failed: entry.txt differs from LINE")
    if not 1 <= len(text) <= CHAR_LIMIT:
        raise ValueError("Character count failed: expected 1 through 88 characters")
    if not 1 <= len(text.split()) <= WORD_LIMIT:
        raise ValueError("Word count failed: expected 1 through 5 words")
    if "\n" in text or "\r" in text:
        raise ValueError("Single-line check failed: found a line break")
    if text.endswith("\n"):
        raise ValueError("Ending check failed: found a trailing newline")
    if text != text.strip():
        raise ValueError("Whitespace check failed: found leading or trailing whitespace")


def main() -> None:
    out_dir = _resolve_output_dir()
    entry = out_dir / "entry.txt"
    entry.write_bytes(LINE.encode("utf-8"))
    validate(entry)
    print(hashlib.sha256(LINE.encode("utf-8")).hexdigest())


if __name__ == "__main__":
    main()
