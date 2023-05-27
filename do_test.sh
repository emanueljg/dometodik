#!/bin/sh

# type check
mypy . --strict

# start up server
flask run &

# run tests
pytest

#kill %-
jobs
sleep 10
jobs
kill %%
jobs
