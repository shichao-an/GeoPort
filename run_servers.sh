#!/bin/bash
# This script is for running dependent servers if none of them are daemons
# on Mac OS X


commands=(
    "mongod --auth"
    "redis-server"
)

if [ "$1" = "start" ]
then
    for command in "${commands[@]}"
    do
        echo "$command"
        $command &
    done
fi

if [ "$1" = "stop" ]
then
    for command in "${commands[@]}"
    do
        pgrep $(echo "$command" | cut -d " " -f 1) | xargs kill
    done
fi
