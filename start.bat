@echo off
title Study Abroad Guide
cd /d "%~dp0"

set PY=
python --version >nul 2>nul && set PY=python
if "%PY%"=="" (py -3 --version >nul 2>nul && set PY=py -3)
if "%PY%"=="" (
  echo.
  echo  Python was not found. Install it from https://www.python.org/downloads/
  echo  IMPORTANT: tick "Add python.exe to PATH" on the first installer screen.
  echo  Then double-click start.bat again.
  echo.
  pause
  exit /b 1
)

if not exist venv (
  echo Creating a private Python environment - first run only...
  %PY% -m venv venv
)
call venv\Scripts\activate.bat

echo Installing needed packages - first run only...
python -m pip install -q -r requirements.txt
if errorlevel 1 (
  echo.
  echo  Package install failed. Check your internet connection and try again.
  pause
  exit /b 1
)

REM open the browser a few seconds after the server starts
start "" cmd /c "timeout /t 3 >nul & start http://localhost:5000"

python app.py
echo.
pause
