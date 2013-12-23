#!/bin/bash
# This script is for exporting pip requirements file with exceptions


# Exceptional packages that will be removed from requirements.txt
exceptions=(
    "cqlengine"
)
sed="sed"
tmp="test_sed.tmp"
brew="/usr/local/bin/brew"
gsed="/usr/local/bin/gsed"
req="requirements.txt"
proj="geoport"
manage="$proj/manage.py"  # manage.py path
bower="$proj/$proj/bower.py"  # `BOWER_INSTALLED_APPS'

# Test sed command
touch $tmp
$sed -i 's/ / /g' $tmp &> /dev/null
if [ "$?" -ne "0" ]
then
    if [ -e "$gsed" ]
    then
        sed="$gsed"
    else
        $brew install gnu-sed
        sed="$gsed"
    fi
fi

pip freeze > $req
echo '# flake8: noqa' > "$bower"  # flake8 exclusion
$manage bower_freeze >> "$bower"

for exception in "${exceptions[@]}"
do
    echo "Removing $exception from $req..."
    $sed -i "/^$exception==/d" $req
done
echo "Export complete."
trap "rm $tmp" EXIT SIGINT SIGQUIT
