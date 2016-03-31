set -e
stack build
stack exec cascadeofinsights clean
stack exec cascadeofinsights watch
