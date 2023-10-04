.PHONY: install format  lint test  sec

install:
	@poetry install

format:
	@blue .
	@isort .

lint:
	@blue . --check
	@isort . --check

test:
	@pytest -v tests
	@python -m unittest tests/test_search_intentions_unittest.py			

sec:
	@pip-audits