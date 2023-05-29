## requirements
* Python 3.10 or higher 
* requirements specified in requirements.txt (installation follows below)

## setup using [venv](https://docs.python.org/3/library/venv.html) (unix)
```sh
# make virtual environment
python -m venv .venv

# activate environment
. .venv/bin/activate

# past this point you should have a (.venv) prompt

# install requirements (flask among others)
pip install -r requirements.txt

# To be able to run pytest's browser tests, you need to init Playwright
playwright install
```

## format and test
```sh
./prepare.sh
```

## quick and dirty setup (not recommended)
For the pragmatic people with no time to make a virtual environemt, you can of course just install the requirements system-wide:
```sh
pip install -r requirements.txt
```

## usage
```sh
# open the website on 127.0.0.1:5000
flask run
```
