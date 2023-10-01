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
	@unittest 

sec:
	@pip-audits