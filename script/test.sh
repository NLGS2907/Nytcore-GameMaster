#!/usr/bin/env bash

clear_screen=false
show_report=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --clear)
            clear_screen=true
            shift
            ;;
        --report)
            show_report=true
            shift
            ;;
        *)
            # Skip unknown arguments
            shift
            ;;
    esac
done

if [[ "$clear_screen" == true ]]; then
    clear
fi

python3.14 -m coverage run -m unittest discover -s . -t . -p "test_*.py" -v --locals

if [[ "$show_report" == true ]]; then
    echo "--- Coverage Report ---"
    python3.14 -m coverage report
fi
