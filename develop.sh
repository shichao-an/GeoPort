#!/bin/bash

pre_commit=".git/hooks/pre-commit"

install_git_hook(){
	cat <<EOL > $pre_commit
#!/bin/bash

folders="geoport"
flake8 $folders
EOL
	chmod +x $pre_commit
}

if [ -z $VIRTUAL_ENV ]
then
	echo "You are not under any virtualenv. Abort."
	exit 1
fi

echo "Installing dependency packages..."
pip install -r requirements.txt

if [ "$?" -ne "0" ]
then
	echo 'Fix system dependencies and use `pip install` to install packages again.'
fi

if [ -d ".git" ]
then
	if [ ! -f $pre_commit ]
	then
		echo "Installing Git hook for flake8..."
		install_git_hook
	fi
else
	echo 'Please clone the repository using `git clone`. Abort.'
	exit 1
fi

echo "Development environment has been set up."
