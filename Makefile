unit-tests:
	pytest --tb=short

unit-watch:
	ls *.py | entr pytest --tb=short

mypy:
	mypy $$(find * -name '*.py')

format:
	black $$(find * -name '*.py')
