#!/bin/bash
# This script is for running dependent servers if none of them are daemons
# on Mac OS X


commands=(
    "mongod --auth"
    "redis-server"
)
usage="./run_servers.sh start|stop"


if [ "$#" -ne 1 ]
then
    echo "$usage"
    exit 1
fi

if [ "$1" = "start" ]
then
    for command in "${commands[@]}"
    do
        echo "$command"
        $command &
    done
    geoport/manage.py supervisor
    exit 0
fi

if [ "$1" = "stop" ]
then
    for command in "${commands[@]}"
    do
        cmd=$(echo "$command" | cut -d " " -f 1)
        pgrep "$cmd" | xargs kill
        echo "$cmd is stopped."
    done
    exit 0
fi

echo "$usage"
exit 1
