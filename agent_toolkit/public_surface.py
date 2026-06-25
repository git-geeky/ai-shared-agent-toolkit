"""Public repository surface scanner.

The built-in rules catch common secret shapes. Deployment-specific literals
belong in a private denylist file passed at runtime.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


DEFAULT_SUFFIXES = {
    ".cfg",
    ".env",
    ".ini",
    ".json",
    ".md",
    ".mjs",
    ".ps1",
    ".py",
    ".sh",
    ".toml",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}

SECRET_PATTERNS = [
    re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    re.compile(r"BEGIN [A-Z ]*PRIVATE KEY"),
    re.compile(r"(?i)(api[_-]?key|access[_-]?token|refresh[_-]?token)\s*[:=]\s*['\"][^'\"]+"),
    re.compile(r"(?i)(password|secret)\s*[:=]\s*['\"][^'\"]+"),
    re.compile(r"(?i)\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
]


@dataclass(frozen=True)
class Finding:
    path: Path
    rule: str


def iter_text_files(root: Path, suffixes: set[str] | None = None) -> Iterable[Path]:
    allowed = suffixes or DEFAULT_SUFFIXES
    for path in root.rglob("*"):
        if ".git" in path.parts or not path.is_file():
            continue
        if path.suffix.lower() in allowed:
            yield path


def load_deny_literals(paths: Sequence[Path], inline: Sequence[str]) -> list[str]:
    literals = [item for item in inline if item]
    for path in paths:
        for line in path.read_text(encoding="utf-8").splitlines():
            value = line.strip()
            if value and not value.startswith("#"):
                literals.append(value)
    return literals


def scan_text(path: Path, text: str, deny_literals: Sequence[str]) -> list[Finding]:
    findings: list[Finding] = []
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            findings.append(Finding(path, pattern.pattern))
    lowered = text.lower()
    for literal in deny_literals:
        if literal.lower() in lowered:
            findings.append(Finding(path, f"literal:{literal}"))
    return findings


def scan_root(root: Path, deny_literals: Sequence[str] = ()) -> list[Finding]:
    findings: list[Finding] = []
    for path in iter_text_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        findings.extend(scan_text(path.relative_to(root), text, deny_literals))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scan a public repo for private surface markers.")
    parser.add_argument("--root", default=".", help="Repository root to scan.")
    parser.add_argument("--deny-file", action="append", default=[], help="Private newline-delimited denylist file.")
    parser.add_argument("--deny-literal", action="append", default=[], help="Additional deny literal.")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    deny_literals = load_deny_literals([Path(item) for item in args.deny_file], args.deny_literal)
    findings = scan_root(root, deny_literals)
    if findings:
        for finding in findings:
            print(f"{finding.path}: {finding.rule}")
        return 1
    print("public surface scan passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
