if ! ps ax | grep -v grep | grep --quiet RedAlert
then
    (python3 -m RedAlert &)
fi
