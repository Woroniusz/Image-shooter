.PHONY: all lint typecheck tests sync

all: sync lint typecheck tests 

sync:
	uv sync --group dev --group gpu

lint:
	uv run ruff check .

typecheck:
	uv run mypy .

tests:
	uv run pytest -v --cov=src --cov-report=term-missing

