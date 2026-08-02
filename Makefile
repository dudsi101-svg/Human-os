.PHONY: install test lint typecheck demo verify

install:
	python -m pip install -e ".[dev]"

test:
	python -m pytest -q

lint:
	python -m ruff check .

typecheck:
	python -m mypy hos_engine

demo:
	python run_demo.py

verify: lint typecheck test
