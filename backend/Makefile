.PHONY: all lint typecheck tests sync

all: sync lint typecheck tests 

sync:
	uv sync --group dev --group gpu
	uv sync --group dev --group gpu --group detectron2

lint:
	uv run ruff check .

typecheck:
	uv run mypy .

tests:
	uv run pytest -v --cov=source_app --cov-report=term-missing

