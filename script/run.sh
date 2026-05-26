#!/bin/bash
possible_ver=( python3.14\ python3\ py\ python)
pyupdate=" -m pip install --upgrade -r requirements.txt"
pyargs=" -m gamemaster"
export BOT_MODE="${1:-test}" # should be available inside the program too

# should change dir to project root
if [[ $PWD == *run ]]
then
    cd ..
fi

for ver in $possible_ver
do
    echo -e "\n\ntrying with '$ver'...\n"
    $ver$pyupdate
    $ver$pyargs
    if [[ $? == 0 ]]
    then
        break
    fi
done
