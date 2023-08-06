{ pkgs ? <nixpkgs> {} }: with pkgs;

let 
  poetry = import ./poetry.nix { inherit pkgs; };
  main = poetry2nix.mkPoetryApplication poetry;
  dev = poetry2nix.mkPoetryApplication (
    poetry // { groups = [ "dev" ]; }
  );

  taskPackages = lib.genAttrs [ "run" "test" "debug" ] 
  (task: let
    isTest = task == "test";
    poetryApp = if !isTest then main else dev;
  in writeShellApplication {
    name = "dometodik-${task}";
    runtimeInputs = [ poetryApp.dependencyEnv ];
    text = let
      playwrightFix = lib.optionalString 
        isTest
        (import ./shellHook.nix { inherit pkgs; });
    in ''
      ${playwrightFix}
      cd ${poetryApp.src.origSrc}
      task ${task}
    '';
  });

in taskPackages // { 
  default = taskPackages.run; 

  # for nix debugging purposes.
  _poetryMain = main; 
  _poetryDev = dev;
}
