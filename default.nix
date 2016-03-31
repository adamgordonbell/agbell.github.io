{ mkDerivation, base, hakyll, stdenv }:
mkDerivation {
  pname = "cascadeofinsights";
  version = "0.1.0";
  src = ./.;
  isLibrary = false;
  isExecutable = true;
  executableHaskellDepends = [ base hakyll ];
  license = stdenv.lib.licenses.unfree;
}
