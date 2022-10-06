#!/bin/bash
# This script executes and removes setup scripts (via trigger)

# This script turn down entire container if some init script is not working
# This can happen when, for example, Django runs before database
set -e

if ! test -f ../blocking.txt; then
    echo 'INFO: blocking.txt is not exist. Initialization...'
    echo 'INFO: Trying to connect to PostrgreSQL for init'

    # Single check variant
    # if test "$(python3 ./postgres-alive.py || echo $?)"; then
    #     echo 'ERROR: Unable to connect to the PostgreSQL database'
    #     echo $'WARNING: Please, reload container and try later (or use `unless-stopped` option)'
    #     echo 'WARNING: Container will exit after 10s...'
    #     sleep 10s
    #     exit 1
    # fi

    for ATTEMPT in $(seq 10)
    do
        if ! test "$(python3 ./postgres-alive.py || echo $?)"; then
            break
        fi

        echo 'ERROR: Unable to connect to the PostgreSQL database'
        echo 'INFO: Retrying after 10s'
        sleep 10s
    done

    if test "$ATTEMPT" = 10; then
        echo 'ERROR: Unable to connect after 10 tries'
        echo 'ERROR: Exiting container'
        exit 1
    fi

    echo 'Successfull connected'

    # SCRIPTS TO BE EXECUTED
    sh migrate.sh
    sh static.sh

    echo 'INIT DONE'

    # Create indicator
    printf "%s\n%s\n" \
        "This file indicator that init.sh must not execute all scripts" \
        "Delete this file for perfom executing all scripts in this folder" > ../blocking.txt
fi
