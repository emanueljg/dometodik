{
  description = "my project description";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.05";

  outputs = { self, nixpkgs }: let 
    system = "x86_64-linux";
    pkgs = import nixpkgs { inherit system; };
    pkg = import ./package.nix { inherit pkgs; };
    devShell = import ./shell.nix { inherit pkgs; };

  in {
    packages.${system}.default = pkg;
    devShells.${system}.default = devShell;
  };
}
