"""Byte fixtures test the inventory, not image decoding or visual quality."""

import contextlib
import csv
import hashlib
import io
from pathlib import Path
import tempfile
import unittest

from audit_images import inventory, main


class InventoryTests(unittest.TestCase):
    def test_recursive_size_hash_order_and_budget(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "nested").mkdir()
            (root / "nested" / "z.PNG").write_bytes(b"abcd")
            (root / "a.webp").write_bytes(b"abc")
            (root / "skip.txt").write_bytes(b"ignored")
            rows = list(inventory(root, 3))
            self.assertEqual([r[0] for r in rows], ["a.webp", "nested/z.PNG"])
            self.assertEqual(rows[0][1:], (3, hashlib.sha256(b"abc").hexdigest(), "ok"))
            self.assertEqual(rows[1][1], 4)
            self.assertEqual(rows[1][3], "over_budget")

    def test_cli_csv_quoting_and_formula_prefix(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "comma,name.png").write_bytes(b"x")
            (root / "=formula.jpg").write_bytes(b"y")
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(main([folder, "--budget-kib", "1"]), 0)
            rows = list(csv.DictReader(io.StringIO(output.getvalue())))
            self.assertEqual(rows[0]["file"], "'=formula.jpg")
            self.assertEqual(rows[1]["file"], "comma,name.png")
            self.assertEqual(rows[1]["bytes"], "1")

    def test_missing_directory_fails(self):
        with tempfile.TemporaryDirectory() as folder:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(main([str(Path(folder) / "missing")]), 2)

    def test_invalid_budget_fails(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as raised:
            main([".", "--budget-kib", "0"])
        self.assertEqual(raised.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
