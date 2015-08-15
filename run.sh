set -e
~/sandbox/stack/dist/build/stack/stack build
~/sandbox/stack/dist/build/stack/stack exec dr-hakyll clean
~/sandbox/stack/dist/build/stack/stack exec dr-hakyll watch
