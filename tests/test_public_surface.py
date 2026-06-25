import re
import unittest
from pathlib import Path


PRIVATE_PATTERNS = [
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
    r"BEGIN [A-Z ]*PRIVATE KEY",
    r"api[_-]?key\s*[:=]\s*['\"][^'\"]+",
    r"token\s*[:=]\s*['\"][^'\"]+",
]


class PublicSurfaceTests(unittest.TestCase):
    def test_no_private_markers(self):
        root = Path(__file__).resolve().parents[1]
        searchable = [".md", ".py", ".json", ".mjs", ".yml", ".toml"]
        offenders = []
        for path in root.rglob("*"):
            if ".git" in path.parts or path.suffix.lower() not in searchable:
                continue
            text = path.read_text(encoding="utf-8")
            for pattern in PRIVATE_PATTERNS:
                if re.search(pattern, text):
                    offenders.append(f"{path.relative_to(root)}:{pattern}")
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
