export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

all: down build up unit-tests

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

build:
	docker compose build

up:
	docker compose up -d api

down:
	docker compose down

e2e-tests: up
	docker-compose run --rm --no-deps --entrypoint=pytest api ./
