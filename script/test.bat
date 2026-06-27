@echo off
setlocal enabledelayedexpansion

set "CLEAR_SCREEN=false"
set "SHOW_REPORT=false"

:parse_args
if "%~1"=="" goto end_parse
if "%~1"=="--clear" set "CLEAR_SCREEN=true"
if "%~1"=="--report" set "SHOW_REPORT=true"
shift
goto parse_args
:end_parse

if "!CLEAR_SCREEN!"=="true" cls

py -m coverage run -m unittest discover -s . -t . -p test_*.py -v --locals

if "!SHOW_REPORT!"=="true" (
    echo --- Coverage Report ---
    py -m coverage report
)

endlocal
