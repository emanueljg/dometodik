#!/bin/sh

# type check
mypy . --strict

# start up server
flask run &

# run tests
pytest

#kill %-
kill %1
