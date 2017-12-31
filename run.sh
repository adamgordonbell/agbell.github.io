set -e
stack setup
stack build
stack exec cascadeofinsights clean
stack exec cascadeofinsights watch
