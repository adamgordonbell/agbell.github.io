set -e
sh runStack --nix setup
sh runStack --nix build
sh runStack --nix exec cascadeofinsights clean
sh runStack --nix exec cascadeofinsights watch
