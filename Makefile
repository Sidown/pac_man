.PHONY: install run debug lint clean

install:
	uv sync

run:
	UV_SKIP_WHEEL_FILENAME_CHECK=1 uv run python -m ghost

debug:
	uv run python -m pdb -m ghost

lint: install
	flake8
	mypy parser --follow-imports=skip --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +
	rm -rf data/output
	rm -rf .venv