#!/bin/sh

set -e

# linter + initial fixes
ruff .

# code format
black .

# type check
mypy . --strict

# start up server
flask run &

# run tests
pytest

# kill server
kill %%
