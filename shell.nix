{ pkgs ? "<nixpkgs>" {} }:

with pkgs; let
  python' = python311.withPackages (p: with p; [
    flask
    flask-login
    playwright
    pytest
    pytest-playwright
    mypy
  ]);
in
mkShell {
  name = "pythonEnv";

  packages = [
    python'
  ];

  shellHook = ''
    export PLAYWRIGHT_BROWSERS_PATH=${playwright-driver.browsers}
  '';
}