# Workflow publishing note

The repository validator is available at `scripts/validate_repository.py`.
The generated GitHub Actions workflow is intentionally not published because
the authenticated OAuth application does not have GitHub's `workflow` scope.
Run the validator locally before each commit.
