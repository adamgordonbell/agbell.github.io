set -e
sh stack setup
sh stack build
sh stack exec cascadeofinsights clean
sh stack exec cascadeofinsights watch
