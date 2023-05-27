#!/bin/sh

# type check
mypy . --strict

# start up server
flask run &

# run tests
pytest

# kills most recent background job (flask server)
kill %%  

