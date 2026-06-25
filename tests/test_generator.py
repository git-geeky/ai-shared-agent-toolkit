import tempfile
import unittest
from pathlib import Path

from agent_toolkit import generator


class GeneratorTests(unittest.TestCase):
    def test_render_agent_context_orders_shared_then_tool_fragments(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "shared" / "context").mkdir(parents=True)
            (root / "tools" / "codex").mkdir(parents=True)
            (root / "shared" / "context" / "a.md").write_text("shared", encoding="utf-8")
            (root / "tools" / "codex" / "head.md").write_text("head", encoding="utf-8")
            (root / "tools" / "codex" / "tail.md").write_text("tail", encoding="utf-8")

            rendered = generator.render_agent_context(root, "codex")

        self.assertIn("GENERATED", rendered)
        self.assertLess(rendered.index("shared"), rendered.index("head"))
        self.assertLess(rendered.index("head"), rendered.index("tail"))

    def test_missing_fragments_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FileNotFoundError):
                generator.render_agent_context(Path(tmp), "codex")


if __name__ == "__main__":
    unittest.main()

