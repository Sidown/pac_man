.PHONY: install run debug lint clean

MAZE_GENERATOR=mazegenerator-00001-py3-none-any.whl
ARGS=json_file/config.json

install:
	uv sync
	UV_SKIP_WHEEL_FILENAME_CHECK=1 uv pip install $(MAZE_GENERATOR)

run: install
	uv run pac-man.py $(ARGS)

debug:
	uv run python -m pdb -m pac-man $(ARGS)

lint: install
	flake8 --extend-exclude .venv
	mypy  . --follow-imports=skip --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +
	rm -rf .venv
