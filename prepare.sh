#!/bin/sh

set -e

# linter + initial fixes
ruff .

# code format
black .

# type check
mypy . --strict

# linter no.2
pylint app tests

# start up server
flask run &

# run tests
pytest

# kill server
kill %%
