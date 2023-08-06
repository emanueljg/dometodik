# Requirements
* Python >= 3.11 
* Python Poetry

# Setup
Install with [Poetry](https://python-poetry.org/docs/#installation).
- Normal installation: `poetry install`
- Include development packages (for running checks): `poetry install --with dev`

After that, instead of prefixing every single command with `poetry run`, you can activate a
virtual environment with `poetry shell`.

Many project workflow commands is implemented with [Taskipy](https://github.com/taskipy/taskipy).
Usage is intuitive; `pytest` -> `task test`, etc. 
Abstracting away the command in question like this allows for implementations to change much more fluidly.
Please refer to `task -l` for a list of available tasks.

# Usage
```sh
# activate venv
poetry shell

# run webserver (gunicorn, probably what you want)
task run
# run webserver (raw flask runner)
task debug
```

# Development
*NOTE:*
- *UPPERCASE* tasks *actively edit* the code if any warnings/errors are automagically fixable.
- *lowercase* tasks *only check* the code.

In the following reference, UPPERCASE tasks are used for checks, but note that non-altering alternatives exist
should you need them.
```sh
  # activate venv
  poetry shell
  
  # run task one by one
  task LINT
  task FORMAT
  task TYPECHECK  
  # run all tasks above (lint + format + typecheck) 
  task CHECK

  # start server in another window
  task debug
  # run e2e tests (requires running server)
  task test

  # run all checks + tests (lint + format + typecheck + test) 
  # requires running server
  task PRECOMMIT
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
  - NixOS module (useful for e.g. dedicated web servers running NixOS) 

Note that you *need* a flake-enabled setup to use this repo.

### Ad-hoc package/app usage
```sh
# Start on localhost port 8000 (gunicorn)
nix run github:emanueljg/dometodik
# or, equivalent:
nix run github:emanueljg/dometodik#run

# start on localhost port 5000 (raw flask run)
nix run github:emanueljg/dometodik#debug

# e2e tests
nix run github:emanueljg/dometodik#test
```

### Module

#### Add to flake inputs
```nix
inputs.dometodik = {
  url = "github:emanueljg/dometodik";
  # useful to avoid unnecessary build time
  #inputs.nixpkgs.follows = "nixpkgs"; 
};
```
#### Module quickstart
This adds a very simple systemd service that starts the webserver on boot.
Website is accessible on `http://127.0.0.1:8000`.
```nix
{ dometodik, ... }: {

  imports = [ dometodik.nixosModules.default ];

  services.dometodik = {
    enable = true;
    openFirewall = true; 
  ];
}
```

#### Example configuration
```nix
{ dometodik, ... }: {

  imports = [ dometodik.nixosModules.default ];

  services.dometodik = {
    enable = true;
    openFirewall = true;
  };

  # setup reverse proxy
  services.nginx = {
    enable = true;
    virtualHosts."example.com" = {
      locations."/".proxyPass = "http://127.0.0.1:8000";

      # ssl stuff
      enableACME = true;
      forceSSL = true;
    };
  };

  security.acme = {
    defaults.email = "johnsmith@example.com";
    acceptTerms = true;
  };
}
```
#### Quick reference
All available module options set to their defaults.
```nix
  services.dometodik = {
    enable = true;  # enable the module
    openFirewall = true;  # open port 80 and 443 in firewall
    nixPackage = pkgs.nixVersions.nix_2_14;  # set nix package to use
    user = "dometodik";  # the user to run the service as
    group = "dometodik";  # the group to run the service as
  };
```

For more details on Nix usage, refer to `flake.nix` (and other `.nix` files)
as well as Nix documentation.





 

