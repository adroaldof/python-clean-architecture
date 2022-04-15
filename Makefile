unit-tests:
	pytest -s --tb=short --pdb --pdbcls=IPython.terminal.debugger:TerminalPdb

unit-watch:
	ls *.py | entr pytest -s --tb=short

isort:
	isort .

lint:
	pylint $$(find * -name '*.py')

mypy:
	mypy $$(find * -name '*.py')

format:
	black $$(find * -name '*.py')
