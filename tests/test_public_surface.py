import unittest
from pathlib import Path

from agent_toolkit import public_surface


class PublicSurfaceTests(unittest.TestCase):
    def test_no_private_markers(self):
        root = Path(__file__).resolve().parents[1]
        deny_literal = "blocked" + ".example.invalid"
        findings = public_surface.scan_root(root, deny_literals=[deny_literal])
        self.assertEqual(findings, [])

    def test_private_deny_literal_is_detected(self):
        deny_literal = "blocked" + ".example.invalid"
        sample_text = "connect to " + deny_literal
        findings = public_surface.scan_text(Path("sample.md"), sample_text, [deny_literal])
        self.assertEqual(len(findings), 1)


if __name__ == "__main__":
    unittest.main()
