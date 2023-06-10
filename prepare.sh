#!/bin/sh

set -e

# hardcore linter
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
