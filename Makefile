unit-tests:
	pytest --tb=short

unit-watch:
	ls *.py | entr pytest --tb=short
