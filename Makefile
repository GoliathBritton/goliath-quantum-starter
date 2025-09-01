test:
	PYTHONPATH=$(PWD)/src pytest --cov=src --cov-report=term-missing tests/

lint:
	black src/ tests/
	flake8 src/ tests/

typecheck:
	mypy src/ tests/

run:
	uvicorn api_server:app --reload
