# Repository Guidelines

## Project Structure & Module Organization

`lettucedetect/` contains the core package: detectors in
`lettucedetect/detectors/`, training and inference in `lettucedetect/models/`,
dataset helpers in `lettucedetect/datasets/`, preprocessing in
`lettucedetect/preprocess/`, prompt templates in `lettucedetect/prompts/`, and
framework integrations in `lettucedetect/integrations/`.

`lettucedetect_api/` contains the FastAPI server, client, and API models. Utility
entry points are in `scripts/`, the configured pytest suite is in `tests/`, docs
are in `docs/`, and static/demo assets are in `assets/` and `demo/`.

## Build, Test, and Development Commands

Install locally with development tools:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Use `pip install -e ".[api]"` for FastAPI support and `pip install -e ".[docs]"`
for documentation tools.

Use `pytest tests/test_inference_pytest.py -v` to run the main suite. To skip
slow model-download tests, run
`pytest tests/test_inference_pytest.py -v -k "not TestAnswerStartToken"`.
Run `ruff format lettucedetect/ tests/` to format, and
`ruff check lettucedetect/ tests/` to lint. Serve docs with `mkdocs serve`.

## Coding Style & Naming Conventions

This project uses Ruff with a 100-character line length. Prefer Python 3.10+
typing such as `list[str]`, `dict[str, Any]`, and `str | None`; use
`from __future__ import annotations` where helpful. Public classes and methods
should have concise docstrings. Use `logging` for runtime messages and
`pathlib.Path` instead of `os.path`.

Name tests as `test_*_pytest.py`, matching the pytest configuration. Keep prompt
template filenames language-specific, for example `qa_prompt_en.txt` or
`summary_prompt_de.txt`.

## Testing Guidelines

Pytest is the test framework, with `pytest-cov` available for coverage checks.
Add core tests under `tests/` and keep model-download or network dependencies
isolated so they can be skipped with `-k`. API smoke tests currently live in
`lettucedetect_api/test_*.py`; include explicit commands for new API-only tests
outside the configured `tests/` path.

## Commit & Pull Request Guidelines

Git history uses short descriptive messages such as `Changes in injector` and
`Better evaluation for code`; no strict Conventional Commits format is enforced.
Use imperative, focused messages and keep each commit scoped to one change.

Pull requests should describe the change, list test and lint commands run, link
related issues, and include screenshots or example output for docs, demo, or
API-facing changes. Avoid bundling unrelated refactors with feature work.

## Security & Configuration Tips

Do not commit API keys, datasets, model checkpoints, or generated outputs.
LLM-based detectors require `OPENAI_API_KEY` in the environment. Large datasets
such as RAGTruth should stay under local data directories and out of version
control unless explicitly documented.
