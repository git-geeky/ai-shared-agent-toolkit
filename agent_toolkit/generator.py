"""Render shared Markdown context into tool-specific agent files."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .restore import load_restore_config, output_path_for_tool


GENERATED_BANNER = "<!-- GENERATED from public ai-shared-agent-toolkit templates. -->"


@dataclass(frozen=True)
class Fragment:
    path: Path
    text: str


def read_fragment(path: Path) -> Fragment:
    return Fragment(path=path, text=path.read_text(encoding="utf-8").strip())


def iter_markdown_files(path: Path) -> Iterable[Path]:
    if not path.exists():
        return []
    return sorted(item for item in path.glob("*.md") if item.is_file())


def collect_fragments(source_root: Path, tool: str) -> list[Fragment]:
    fragments: list[Fragment] = []
    shared_context = source_root / "shared" / "context"
    fragments.extend(read_fragment(path) for path in iter_markdown_files(shared_context))

    tool_root = source_root / "tools" / tool
    for name in ("head.md", "tail.md"):
        path = tool_root / name
        if path.exists():
            fragments.append(read_fragment(path))
    return fragments


def render_agent_context(source_root: Path, tool: str) -> str:
    fragments = collect_fragments(source_root, tool)
    if not fragments:
        raise FileNotFoundError(f"no markdown fragments found for tool {tool!r}")
    body = "\n\n".join(fragment.text for fragment in fragments if fragment.text)
    return f"{GENERATED_BANNER}\n\n{body}\n"


def resolve_output_path(args: argparse.Namespace) -> Path:
    if args.out:
        return Path(args.out)
    restore = load_restore_config()
    restored = output_path_for_tool(args.tool, restore)
    if restored:
        return restored
    return Path("dist") / args.tool / "AGENTS.md"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render generic shared agent context.")
    parser.add_argument("--source", default=".", help="Template source root.")
    parser.add_argument("--tool", required=True, help="Tool adapter name, for example codex.")
    parser.add_argument("--out", default=None, help="Output path. Overrides restore overlay.")
    args = parser.parse_args(argv)

    source_root = Path(args.source)
    output_path = resolve_output_path(args)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_agent_context(source_root, args.tool), encoding="utf-8")
    print(str(output_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

