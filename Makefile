install:
	uv sync

run:
	uv run python3 main.py

debug:
	uv run python3 -m debugpy main.py

lint:
	uv run flake8
	uv run mypy .

lint-strict:
	uv run flake8
	uv run mypy --strict .

clean:
	rm -rf .mypy_cache
	rm -rf `find . -type d -name "__pycache__"`

fclean: clean
	rm -rf .venv
	rm -rf uv.lock

.PHONY: install run debug lint lint-strict clean fclean