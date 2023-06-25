.PHONY: run-server
run-server:
	python manage.py runserver

.PHONY: lint
lint: clean
	black .
	isort .
