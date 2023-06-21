#!/bin/bash

# not using checkAlive for now...

# # echo hello
# cd $( realpath $(dirname -- "$0") )

# # LOG_FILE=./last_check_alive.txt
# echo $(date)
# ps ax | grep -v grep | grep "python -m RedAlert"

# if ! ps ax | grep -v grep | grep --quiet "python -m RedAlert"
# then
#     echo "starting new"
#     # echo $PATH
#     # echo PIPENV=$PIPENV 
#     # set PIPENV to /home/<username>/.local/bin/pipenv or whereis pipenv
#     (/home/erasta/.local/bin/pipenv run python -m RedAlert --posts &) >> last_check_alive.txt 2>&1
# else
#     echo "all is good not starting"
# fi

