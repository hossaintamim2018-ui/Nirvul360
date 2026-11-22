# Contributing to Nirvul360

Thank you for contributing to Nirvul360. To maintain clean repo hygiene and high code quality, please adhere to the guidelines below.

## Branch Strategy

- `main`: Production-ready branch. All commits must pass CI checks.
- Feature branches: Use descriptive prefixes like `feat/`, `fix/`, `refactor/`, `chore/` (e.g., `feat/pos-image-sync`).

## Pull Request Process

1. Create a feature branch from the latest `main`.
2. Ensure backend tests pass:
   ```bash
   pytest backend/tests/ -v
   ```
3. Ensure frontend builds and passes smoke checks:
   ```bash
   npm run build:frontend
   npm run test:frontend
   ```
4. Verify code format and linter rules with `ruff check backend/`.
5. Submit a Pull Request targeting `main` with a clear description of changes.

## Double-Entry Accounting Rule

All financial ledger transactions must strictly satisfy:
`SUM(debit) == SUM(credit)`
Never mutate historical purchase price records or skip ledger reconciliation.
