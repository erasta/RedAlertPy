# echo hello
cd $( realpath $(dirname -- "$0") )

LOG_FILE=./last_check_alive.txt
echo $(date) > $LOG_FILE
ps ax | grep -v grep | grep "python -m RedAlert" >> $LOG_FILE

if ! ps ax | grep -v grep | grep --quiet "python -m RedAlert"
then
    echo "starting new" >> $LOG_FILE
    (pipenv run python -m RedAlert --posts &)
else
    echo "all is good not starting" >> $LOG_FILE
fi
