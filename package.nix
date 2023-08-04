{ pkgs ? <nixpkgs> {} }:

pkgs.poetry2nix.mkPoetryApplication (
  import ./poetry.nix { inherit pkgs; }
)
