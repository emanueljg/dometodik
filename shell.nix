{ 
  pkgs ? <nixpkgs> {}
}:

with pkgs; 
with (import (fetchFromGitHub {
  owner = "NixOS";
  repo = "nixpkgs";
  rev = "131808261a30a2dd9742098a2a5d864dbc70cfc5";
  sha256 = "sha256-NNxdrVRooAiqMWUwjer+gc2cGfx4buijhtPydPzg4gM=";
}) { inherit system; }).rustPlatform;  # 1.70
let
  nixpkgsMaster = (import (fetchFromGitHub {
    owner = "NixOS";
    repo = "nixpkgs";
    rev = "131808261a30a2dd9742098a2a5d864dbc70cfc5";
    sha256 = "sha256-NNxdrVRooAiqMWUwjer+gc2cGfx4buijhtPydPzg4gM=";
  }) { inherit system; });

  inherit (nixpkgsMaster) rustPlatform playwright-driver;
  
  overrides = with python311Packages; poetry2nix.defaultPoetryOverrides.extend
  (self: super: {

    ruff = super.ruff.overridePythonAttrs (old: rec {
      src = fetchFromGitHub {
        owner = "astral-sh";
        repo = "ruff";
        rev = "v${old.version}";
        sha256 = "sha256-B4wZTKC1Z6OxXQHrG9Q9VjY6ZnA3FOoMMNfroe+1A7I=";
      };

      cargoDeps = importCargoLock {
        lockFile = "${src}/Cargo.lock";
        outputHashes = {
          "libcst-0.1.0" = "sha256-jG9jYJP4reACkFLrQBWOYH6nbKniNyFVItD0cTZ+nW0=";
          "ruff_text_size-0.0.0" = "sha256-5CjNHj5Rz51HwLyXtUKJHmEKkAC183oafdqKDem69oc=";
          "unicode_names2-0.6.0" = "sha256-eWg9+ISm/vztB0KIdjhq5il2ZnwGJQCleCYfznCI3Wg=";
        };
      };

      nativeBuildInputs = (old.nativeBuildInputs or [ ]) ++ [
        cargoSetupHook
        maturinBuildHook
      ];
    });

    taskipy = super.taskipy.overridePythonAttrs (old: {
        buildInputs = (old.buildInputs or [ ]) ++ [ super.poetry ];
    });

    pytest-base-url = super.pytest-base-url.overridePythonAttrs (old: {
        buildInputs = (old.buildInputs or [ ]) ++ [ super.poetry super.setuptools ];
    });

    pytest-playwright = super.pytest-playwright.overridePythonAttrs (old: {
        buildInputs = (old.buildInputs or [ ]) ++ [ super.setuptools super.setuptools-scm ];
    });

    urllib3 = super.urllib3.overridePythonAttrs (old: {
        buildInputs = (old.buildInputs or [ ]) ++ [ super.hatchling ];
    });

    # playwright = let 
    #   playwright-driver = pkgs.playwright-driver.overrideAttrs (final: prev: {
    #     inherit (super.playwright) version;
    #     src = let 
    #       filename = "playwright-${final.version}-linux.zip";
    #     in fetchurl {
    #       url = "https://playwright.azureedge.net/builds/driver/${filename}"; 
    #       sha256 = "sha256-fOzqH89jnSpyUltbFyr83mclYfy5CLrk+npFfT2CV+c=";
    #     };
    #   });
    # in (super.playwright.override { inherit playwright-driver; }).overridePythonAttrs (
    #   prev: {
    #     propagatedBuildInputs = (prev.propagatedBuildInputs or [ ]) ++ [(
    #       writeShellScriptBin "playwrightx" ''
    #         export PLAYWRIGHT_BROWSERS_PATH=${playwright-driver.browsers}
    #         ${prev.src}/bin/playwright
    #       ''
    #     )];
    #   });
  }); 
  poetryEnv = poetry2nix.mkPoetryEnv {
    projectDir = ./.;
    python = pkgs.python311;
    inherit overrides;
  };
in poetryEnv.env.overrideAttrs (_: {
  shellHook = ''
    export PLAYWRIGHT_BROWSERS_PATH=${playwright-driver.browsers}
  '';
})
