set -e
~/sandbox/stack/dist/build/stack/stack build
~/sandbox/stack/dist/build/stack/stack exec cascadeofinsights clean
~/sandbox/stack/dist/build/stack/stack exec cascadeofinsights watch
