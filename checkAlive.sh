# echo hello
cd $( realpath $(dirname -- "$0") )
# ps ax | grep -v grep | grep "python -m RedAlert"

if ! ps ax | grep -v grep | grep --quiet "python -m RedAlert"
then
    (pipenv shell && python3 -m RedAlert --posts &)
    # echo not running
# else
#     echo running
fi
