export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

all: down build up unit-tests

isort:
	isort .

format:
	black $$(find * -name '*.py')

lint:
	pylint $$(find * -name '*.py')

mypy:
	mypy $$(find * -name '*.py')

unit-watch:
	ls *.py | entr pytest -s --tb=short

build:
	docker compose build

up:
	docker compose up -d api

down:
	docker compose down

logs:
	docker compose logs -f api --tail=100

unit-tests:
	docker compose run --rm --no-deps api pipenv run pytest ./tests/unit

integration-tests: up
	docker compose run --rm --no-deps api pipenv run pytest ./tests/integration

e2e-tests: up
	docker compose run -e API_HOST=api --rm --no-deps api pipenv run pytest ./tests/e2e

tests: up
	docker compose run -e API_HOST=api --rm --no-deps api pipenv run pytest ./tests/unit ./tests/integration ./tests/e2e
