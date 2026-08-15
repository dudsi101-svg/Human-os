.PHONY: install test lint typecheck demo run-app verify

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

run-app:
	python -m pip install -e ".[app]"
	FLASK_APP=app.server:create_app python -m flask run

verify: lint typecheck test
