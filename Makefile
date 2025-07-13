.PHONY: lint test run

lint:
	ruff check .

test:
	pytest

run:
	python main.py https://example.com -o sample.json
