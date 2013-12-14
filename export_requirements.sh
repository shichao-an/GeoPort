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

for exception in "${exceptions[@]}"
do
    echo "Removing lines containing $exception from $req..."
    $sed -i '/cqlengine/d' $req
done
echo "Export complete."
trap "rm $tmp" EXIT SIGINT SIGQUIT
