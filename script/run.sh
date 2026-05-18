#!/bin/bash
possible_ver=( python3.13\ python3\ py\ python)
pyupdate=" -m pip install --upgrade -r requirements.txt"
pyargs=" -m gamemaster"

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
