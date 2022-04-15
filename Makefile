unit-tests:
	pytest --tb=short

unit-watch:
	ls *.py | entr pytest --tb=short

isort:
	isort .

lint:
	pylint $$(find * -name '*.py')

mypy:
	mypy $$(find * -name '*.py')

format:
	black $$(find * -name '*.py')
