test:
	uv run python -m unittest discover
	uv run ruff format
	uv run ruff check
	uv run ty check
