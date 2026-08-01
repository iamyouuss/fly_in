install:
	uv sync

run:
	uv run python3 main.py $(ARGS)

debug:
	uv run python3 -m pdb main.py $(ARGS)

lint:
	uv run flake8 src/
	uv run mypy src/ 

lint-strict:
	uv run flake8 src/
	uv run mypy --strict src/
clean:
	rm -rf .mypy_cache
	rm -rf `find . -type d -name "__pycache__"`

fclean: clean
	rm -rf output.txt
	rm -rf .venv
	rm -rf uv.lock

.PHONY: install run debug lint lint-strict clean fclean