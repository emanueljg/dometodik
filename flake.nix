{
  description = "my project description";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.05";

  outputs = { self, nixpkgs }: let 
    system = "x86_64-linux";
    pkgs = import nixpkgs { inherit system; };
    inherit (pkgs) callPackage;
    
    packages = import ./packages.nix { inherit pkgs; };
    devShell = callPackage ./shell.nix { };
    module = import ./module.nix;
    # devShell = import ./shell.nix { inherit pkgs; };

  in {
    packages.${system} = packages;
    devShells.${system}.default = devShell;
    nixosModules."dometodik" = module;
    nixosModules.default = module;
  };
}
