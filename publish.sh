set -e
set -x
function pause(){
   echo " enter to continue.  Ctrl-C to bail"
   read -p "$*"
}

echo "All work must be commited in hakyll before running"
pause
rm -rf /_site
git submodule init
git submodule update
cd _site
git pull origin master
git checkout master
cd ..
stack setup
stack build
# not needed bc removed
#stack exec cascadeofinsights clean
stack exec cascadeofinsights build

cd _site/
git add .
git commit -m "Update [ci skip]"
git push origin master
cd ..
git add _site/
git add .
git commit -m "Update [ci skip]"
git push origin hakyll
