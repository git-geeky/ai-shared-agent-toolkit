# AI Shared Agent Toolkit

Generic building blocks for keeping agent configuration consistent across
multiple local AI coding tools.

This public extract includes:

- a small Markdown context generator;
- an optional private restore overlay loaded from outside git;
- hook-policy helpers for command/path classification;
- generic skill and CI templates;
- lightweight memory-audit schemas.
- a public-surface scanner that can consume a private denylist outside git.

It intentionally excludes private machine paths, service inventories, tokens,
logs, session transcripts, decrypted secrets, and local runtime state.

## Restore Overlay

The repo stays generic. Machine-specific paths can be supplied through a private
JSON file outside git:

```powershell
$env:AI_SHARED_TOOLKIT_RESTORE_FILE = "$env:LOCALAPPDATA\ai-shared-agent-toolkit\restore.local.json"
python -m agent_toolkit.generator --source examples --tool codex --out dist/codex/AGENTS.md
```

Start from `config/restore.example.json` and keep your local file untracked.

## Quick Start

```powershell
python -m unittest discover -s tests
python -m agent_toolkit.generator --source examples --tool codex --out dist/codex/AGENTS.md
node --check shared/hooks/policy.mjs
python -m agent_toolkit.public_surface --root . --deny-literal private.example
```

The generated file is assembled from:

1. `shared/context/*.md`
2. `tools/<tool>/head.md`
3. `tools/<tool>/tail.md`

The restore overlay may define output paths per tool, but it is never required
for tests or for generating portable examples.

## Public Surface Checks

`agent_toolkit.public_surface` scans text files for common secret patterns and
optional deployment-specific literals supplied at runtime:

```powershell
python -m agent_toolkit.public_surface --root . --deny-file C:\path\to\private-denylist.txt
```

Keep the denylist file private. The scanner is designed so public repos can use
the same boundary-checking workflow without committing private terms.
