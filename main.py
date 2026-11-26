"""One Word, One Username, One Reward — entry program.

Writes the entrant's own make.fun username, and nothing else, to
/output/entry.txt. The username is the account's genuine handle
(ridwan-sumantoro), one word, 16 characters.

Deterministic: no network, no randomness, no secrets, no clock. The
competition's gate is self-checked before anything is written, and the
judge brief's single-word rule is checked too: no spaces, no padding,
no gloss tacked on. If any check fails, nothing is written and the run
exits non-zero.

Usage:
    python3 main.py              # writes /output/entry.txt (or $ENTRY_OUTPUT_DIR/entry.txt)
    python3 main.py --self-test  # validates the gate logic, writes nothing
"""

import os
import sys

WORD = "ridwan-sumantoro"
MAX_CHARS = 30


def check_gate(word: str) -> None:
    """Enforce the sealed scorer's gate plus the single-word rule.

    Gate: UTF-8 text of 1 to 30 characters, not only whitespace.
    Single-word rule: no whitespace anywhere in the entry.
    """
    if not isinstance(word, str):
        raise ValueError("entry is not text")
    encoded = word.encode("utf-8")  # raises if not UTF-8 text
    if not 1 <= len(word) <= MAX_CHARS:
        raise ValueError(f"entry is {len(word)} chars, gate needs 1-30")
    if not word.strip():
        raise ValueError("entry is only whitespace")
    if any(ch.isspace() for ch in word):
        raise ValueError("entry contains whitespace, not a single word")
    if word != word.strip():
        raise ValueError("entry has leading/trailing padding")
    if len(encoded) != len(word):
        raise ValueError("entry is not plain ASCII text")


def self_test() -> int:
    """Exercise the gate on good and bad inputs; writes nothing."""
    check_gate(WORD)
    bad = ["", " " * 5, "x" * 31, "two words", " padded", "padded ",
           "tab\there", "new\nline"]
    for sample in bad:
        try:
            check_gate(sample)
        except ValueError:
            continue
        print(f"self-test FAILED: gate accepted {sample!r}")
        return 1
    print(f"self-test passed: {WORD!r} ({len(WORD)} chars) valid, "
          f"{len(bad)} bad inputs rejected")
    return 0


def main(argv) -> int:
    if argv == ["--self-test"]:
        return self_test()
    if argv:
        print(f"unknown arguments: {argv}", file=sys.stderr)
        return 2
    check_gate(WORD)
    out_dir = os.environ.get("ENTRY_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(WORD)
    print(f"wrote {len(WORD)} chars to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
