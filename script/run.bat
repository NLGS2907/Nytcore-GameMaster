@echo off
set possible_ver= python3.13 python3 py python
set pyupdate= -m pip install --upgrade -r requirements.txt
set pyargs= -m gamemaster

@REM should change dir to project root
if %CD:~-3% == run (
    cd ..
)

for %%v in (%possible_ver%) do (
    echo: & echo: & echo Trying with '%%v'...& echo:
    %%v%pyupdate%%reqpath%
    %%v%pyargs%
    if not errorlevel 1 goto:EOF
)
