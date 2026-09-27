@echo off
cd /d "%~dp0"
py -3 run.py serve --port 8765
pause
