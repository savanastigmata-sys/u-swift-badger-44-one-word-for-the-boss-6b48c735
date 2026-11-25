"""One Word for the Boss — make.fun entry.

Writes exactly one word describing the boss to entry.txt.

The word is the whole entry: a single word, no phrase, no caption,
no explanation, at most 30 characters. The grader reads
$MAKEFUN_OUTPUT_DIR/entry.txt (the sandbox mounts it at /output).
"""

import os
import sys

# The entry: one word for the boss. Funny, true, fresh.
# The boss who texts at midnight — and expects an answer by morning.
WORD = "Midnighttexter"

MAX_CHARS = 30


def resolve_output_dir():
    """Return the directory the entry text goes in.

    The grader sets MAKEFUN_OUTPUT_DIR; fall back to ./output so the
    program also runs standalone.
    """
    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if out:
        return out
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")


def validate(word):
    """Enforce the competition's entry format.

    Exactly one word: 1-30 characters, a single line, no spaces,
    not only whitespace, no control characters, and at least one
    letter so the entry is a word rather than punctuation.
    """
    if not isinstance(word, str):
        raise ValueError("entry must be a string")
    if not word or word != word.strip():
        raise ValueError("entry must not be empty or padded with whitespace")
    if len(word) > MAX_CHARS:
        raise ValueError("entry is %d characters, over the %d limit"
                         % (len(word), MAX_CHARS))
    if any(ch.isspace() for ch in word):
        raise ValueError("entry must be a single word with no spaces")
    if "\n" in word or "\r" in word:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in word):
        raise ValueError("entry must not contain control characters")
    if not any(ch.isalpha() for ch in word):
        raise ValueError("entry must contain at least one letter")
    return word


def main():
    word = validate(WORD)
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(word + "\n")
    # Round-trip check: what landed on disk must be exactly the
    # validated word plus one newline, so two runs are byte-identical.
    with open(path, "rb") as fh:
        raw = fh.read()
    if raw != (word + "\n").encode("utf-8"):
        raise RuntimeError("entry.txt round-trip mismatch: %r" % raw)
    print("wrote %s (%d chars)" % (path, len(word)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
