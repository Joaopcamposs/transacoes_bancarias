ruff:
	ruff format . && ruff check . --fix

run:
	fastapi dev main.py