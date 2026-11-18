# Contributing

## Branches

- Use `main` only for reviewed, passing changes.
- Create a short-lived branch for work:
  `feature/<task-id>-<short-name>`, `fix/<task-id>-<short-name>`, or
  `docs/<task-id>-<short-name>`.
- Open a pull request and require a clean CI run before merging.

## Commits

Use a conventional commit prefix and the task ID when applicable:

```text
feat: add fence crossing alert
fix(F1-03): reject invalid auth scope
docs(F0-04): record repository layout ADR
chore: pin development runtime
test: cover deny-by-default authorization
```

## Code rules

- Follow the authoritative PRD/TRD contracts; do not invent fields or states.
- Keep tasks at eight person-hours or less.
- Update the task board when estimates or dependencies change.
- Add focused tests for behavior that is introduced or changed.
- Keep P0 vertical-slice work passing before starting optional P1/P2 features.
- Never commit credentials, private datasets, licensed media, model weights,
  or operational footage.
