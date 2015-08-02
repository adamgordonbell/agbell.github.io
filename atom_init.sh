ln -s codex.tags .tags
# for dash
cabal sandbox init
cabal install --only-dependencies --enable-documentation --reinstall
# dash-haskell -c scheme48.cabal
codex update
