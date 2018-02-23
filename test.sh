repo=$(basename $PWD)
nosetests --with-coverage --cover-package=$repo
