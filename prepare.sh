#!/bin/sh

# code format
black .

# type check
mypy . --strict

# start up server
flask run &

# run tests
pytest

kill %%
#kill %1
