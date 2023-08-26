.PHONY: lint

lint:
	black .
	isort .
