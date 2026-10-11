"""Inventory image-named files locally; no decoding, conversion or network access."""

import argparse
import csv
import hashlib
from pathlib import Path
import sys

EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".avif", ".gif", ".heic", ".heif", ".svg"}


def inventory(root, budget_bytes):
    """Yield relative name, bytes, digest and budget flag in stable filename order."""
    root = Path(root)
    if not root.is_dir():
        raise ValueError("Input must be an existing directory")
    for path in sorted(root.rglob("*")):
        if path.is_symlink() or not path.is_file() or path.suffix.lower() not in EXTENSIONS:
            continue
        digest = hashlib.sha256()
        size = 0
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                size += len(chunk)
                digest.update(chunk)
        name = path.relative_to(root).as_posix()
        # Neutralize spreadsheet formula prefixes in user-controlled filenames.
        if name.startswith(("=", "+", "-", "@", "\t", "\r", "\n")):
            name = "'" + name
        yield name, size, digest.hexdigest(), "over_budget" if size > budget_bytes else "ok"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--budget-kib", type=int, default=300, help="Per-file budget in KiB (default: 300)")
    args = parser.parse_args(argv)
    if args.budget_kib < 1:
        parser.error("--budget-kib must be a positive integer")
    try:
        writer = csv.writer(sys.stdout, lineterminator="\n")
        writer.writerow(("file", "bytes", "sha256", "budget_status"))
        for row in inventory(args.directory, args.budget_kib * 1024):
            writer.writerow(row)
    except (OSError, ValueError) as error:
        print(f"Inventory failed: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
