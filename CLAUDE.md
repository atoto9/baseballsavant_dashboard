# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working in this repository.

## Build & Run Commands
- Build & run: `docker-compose up -d --build`
- Run without rebuild: `docker-compose up -d`
- Stop services: `docker-compose down`
- Run dashboard standalone: `python app.py`
- Deploy with Gunicorn: `gunicorn --workers 4 --bind 0.0.0.0:8050 app:server`

## Test Commands
- Install dev dependencies: `pip install -r requirements-dev.txt`
- Run all tests: `pytest`
- Run specific test file: `pytest tests/components/test_charts.py`
- Run specific test: `pytest tests/utils/test_data_processing.py::test_process_pitcher_data`
- Run with coverage: `pytest --cov=.`
- Run only unit tests: `pytest -m unit`

## Code Style Commands
- Format code: `black .`
- Lint code: `flake8`
- Type check: `mypy .`

## Code Style Guidelines
- Format Python code with 4-space indentation
- Use docstrings for functions/components (see charts.py)
- Class names: PascalCase
- Function/variable names: snake_case
- Import order: standard library → third-party → local modules
- Error handling: wrap database calls in try/except with meaningful error messages
- Type annotations not currently used but preferred for new code
- Follow existing patterns in component organization (see components/charts.py)
- Include descriptive comments for complex data processing
- Maintain consistent chart styling with existing charts