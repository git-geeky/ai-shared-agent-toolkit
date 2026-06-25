import json
import os
import tempfile
import unittest
from pathlib import Path

from agent_toolkit import restore


class RestoreTests(unittest.TestCase):
    def test_restore_file_is_optional(self):
        self.assertEqual(restore.load_restore_config(env_var="MISSING_AGENT_TOOLKIT_RESTORE_ENV"), {})

    def test_explicit_restore_file_loads_output_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "restore.local.json"
            path.write_text(json.dumps({"outputs": {"codex": "D:/agent/AGENTS.md"}}), encoding="utf-8")
            old = os.environ.get(restore.RESTORE_FILE_ENV)
            os.environ[restore.RESTORE_FILE_ENV] = str(path)
            try:
                payload = restore.load_restore_config()
                output_path = restore.output_path_for_tool("codex", payload)
            finally:
                if old is None:
                    os.environ.pop(restore.RESTORE_FILE_ENV, None)
                else:
                    os.environ[restore.RESTORE_FILE_ENV] = old

        self.assertEqual(str(output_path).replace("\\", "/"), "D:/agent/AGENTS.md")


if __name__ == "__main__":
    unittest.main()

