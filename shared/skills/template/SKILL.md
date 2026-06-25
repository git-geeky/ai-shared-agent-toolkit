# Skill Template

Use this template when a workflow should be reusable across agent harnesses.

## Purpose

Describe the task shape this skill handles and when it should not be used.

## Inputs

- Repository or workspace path.
- User-supplied goal.
- Optional private restore file for local paths.

## Procedure

1. Inspect the current state before editing.
2. Identify private or environment-specific values.
3. Make the smallest useful change.
4. Run the relevant verification gate.
5. Report changed files, commands run, and remaining assumptions.

## Safety

Never include credentials, decrypted secrets, raw session transcripts, or local
machine inventory in public artifacts.

