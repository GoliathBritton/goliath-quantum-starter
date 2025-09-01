# Contributing

## Branching & PRs
- `main` is protected.
- Create feature branches: `feat/<slug>`.
- Open PRs with:
  - Linked issue
  - Checklist: tests, docs, LTC reference
  - At least 1 reviewer (core-maintainers)

## Style & Quality
- black, ruff, mypy
- pytest with coverage ≥ 85% for src/nqba
- No failing ruff rules at commit

## Commit Messages
- Conventional Commits: feat:, fix:, docs:, chore:, refactor:, test:

## Code Owners (suggested)
```
# CODEOWNERS
/src/nqba/ @core-maintainers
/docs/     @tech-writers @core-maintainers
```
