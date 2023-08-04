{ pkgs ? <nixpkgs> {} }:
  with pkgs; 
let
  # grab a playwright-driver that matches playwright
  inherit (import (fetchFromGitHub {
    owner = "NixOS";
    repo = "nixpkgs";
    rev = "131808261a30a2dd9742098a2a5d864dbc70cfc5";
    sha256 = "sha256-NNxdrVRooAiqMWUwjer+gc2cGfx4buijhtPydPzg4gM=";
  }) { inherit system; }) playwright-driver;

  poetryEnv = poetry2nix.mkPoetryEnv (import ./poetry.nix { inherit pkgs; });

in poetryEnv.env.overrideAttrs (_: {
  shellHook = ''
    export PLAYWRIGHT_BROWSERS_PATH=${playwright-driver.browsers}
  '';
})
