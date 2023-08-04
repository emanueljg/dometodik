## requirements
* Python >= 3.11 
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

## lint, format and test
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

## Code explanation
The site is built using Flask, the same "framework" we used
for auctionista (the database course). 
The basic model works as follows:
```py
@app.route('/thing')  # do this for route /thing 
def thing():
  return '<h1>Hello world</h1>'  # return html like this
  return render_remplate("file.html")  # or like this
```
The way this website is designed is that we basically only have one main route, that being
the `content_route` route. This is a metaroute that catches all of registered content routes (`/home`, `/members`, etc) 
and sends it forward to a function which renders base html, 
in other words the same base html which we get from the base route `/`. But then how does different content gets shown
if we render the base html? By sending the currently routed content as a variable in the base html through
the magic of Jinja html templating. Doing this, we can decide in the base html what content-html to render,
as well as style the selected content correctly. Both the buttons and the "text in the box" can be considered as
part of a Content object. A more technical description of this can be found in the documentation of 
`helpers.elems_with_attrs`. 

That's the gist of it. Read up on the code internals to understand in detail how it all plays out. You have to really
make an effort to understand it or you will feel hopeless when using it. Try adding other
`Content` objects yourself to cement your understanding of it.

If you're adding a new feature, be sure to add test(s) for it in `tests/test_<your feature>.py`. A feature without
tests is an antifeature.

Also - this code has strict checks and if you don't check the code you commit it's not going to pass. Run the tests
locally before making a PR. 


## Nix usage
This repository supports nix usage through `flake.nix`, which contains two parts:
  - Runnable package(s)
  - NixOS module (useful for e.g. web servers running NixOS) 

### Ad-hoc package/app usage
```sh
# Start on localhost port 8000 (gunicorn)
nix run github:emanueljg/dometodik#run
# or, equivalent:
nix run github:emanueljg/dometodik

# start on localhost port 5000 (raw flask run)
nix run github:emanueljg/dometodik#debug

# e2e tests
nix run github:emanueljg/dometodik#test
```

### Module usage
Planned but not implemented yet. 


For more details, refer to `flake.nix` as well as Nix documentation.





 

