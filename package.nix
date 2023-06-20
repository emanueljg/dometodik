{ 
  pkgs ? "<nixpkgs>", 
  python ? pkgs.python3
}:

pkgs.poetry2nix.mkPoetryApplication {
  projectDir = ./.;
  inherit python;
}
