# Architecture Patterns with Python code Sample

Practice repo to follow the [Architecture Patterns with Python](https://www.oreilly.com/library/view/architecture-patterns-with/9781492052197/) suggested project

The project is using [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/). Also it has a `Makefile` to help running the most used commands

## Code Quality

In order to keep the code quality is being used [isort](https://pycqa.github.io/isort/), [black](https://github.com/psf/black), [pylint](https://www.pylint.org/) and [mypy](http://www.mypy-lang.org/) that can be used with the follow commands:

```bash
make isort
make black
make pylint
make mypy
```

## Tests

The tests can be run according your needs

```bash
make unit-tests
make integration-tests
make e2e-tests
```

There is also a possibility to run all tests in sequence at once

```bash
make tests
```

## One Last Thing

All the commands above will run once a push is made to the repository

---

Enjoy id :+1:
