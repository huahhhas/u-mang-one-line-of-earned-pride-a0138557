#!/usr/bin/env python3
"""One Line of Earned Pride — make.fun bounty entry.

Writes one original line to /output/entry.txt (or $OUTPUT_DIR/entry.txt
for local runs). Pure Python 3 standard library, no dependencies,
fully deterministic: the same bytes every run.
"""

import hashlib
import os

LINE = (
    "I carried the last box up four flights alone, set it down in my own "
    "empty flat, and sat on the floor because the key in my pocket was "
    "finally mine."
)


def validate(text: str) -> bytes:
    """Fail fast on a line that would fail the gate, before touching output."""
    data = text.encode("utf-8")
    if not 1 <= len(text) <= 240:
        raise ValueError(f"entry must be 1-240 characters, got {len(text)}")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if text != text.strip():
        raise ValueError("entry must not start or end with whitespace")
    return data


def main() -> None:
    data = validate(LINE)
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # Atomic write: a bad run never leaves a half-written entry behind.
    tmp_path = path + ".tmp"
    with open(tmp_path, "wb") as f:
        f.write(data)
    os.replace(tmp_path, path)
    raw = open(path, "rb").read()
    text = raw.decode("utf-8")
    assert raw == data
    assert text == LINE
    print("sha256:", hashlib.sha256(raw).hexdigest())
    print("chars:", len(text), "bytes:", len(raw))


if __name__ == "__main__":
    main()
