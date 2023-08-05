{ config, pkgs, lib, ... }: with lib; let
  cfg = config.services.dometodik;
  name = "dometodik";
in {
  options.services.${name} = with types; {
    enable = mkEnableOption name;

    flake = mkOption {
      type = submodule { options = {
        path = mkOption {
          type = either str path;
          default = ./.;
        };
        outputAttr = mkOption {
          type = str;
          default = "";
        };
      };};
      default = { };
    };

    openFirewall = mkOption {
      type = bool;
      default = false;
    };
      
    nixPackage = mkOption {
      type = package;
      default = pkgs.nixVersions.nix_2_14;
    };

    user = mkOption {
      type = str;
      default = name;
    };

    group = mkOption {
      type = str;
      default = name;
    };

  };

  config = mkIf cfg.enable {

    users = {

      users.${name} = mkIf (cfg.user == name) {
        isSystemUser = true;
        group = cfg.group;
      };

      groups.${name} = mkIf (cfg.group == name) { };
    };

    systemd = let
      WorkingDirectory = "/var/${name}";
    in {
      tmpfiles.rules = [
        "D ${WorkingDirectory} 774 ${cfg.user} ${cfg.group} -"
      ];
      services.${name} = {
        wantedBy = [ "multi-user.target" ];
        after = [ "network-online.target" ];
        environment.HOME = WorkingDirectory;
        script = with cfg.flake; let
          nix = "${cfg.nixPackage}/bin/nix";
          flake = "path:${path}#${outputAttr}";
        in "${nix} run ${flake}";
        serviceConfig = {
          User = cfg.user;
          Group = cfg.group;
          inherit WorkingDirectory;
        };
      };
    };

    networking.firewall.allowedTCPPorts = mkIf cfg.openFirewall [ 80 443 ];

  };

}
        
