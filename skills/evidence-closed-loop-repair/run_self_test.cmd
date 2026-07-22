@echo off
python "%~dp0scripts\self_test.py"
if errorlevel 1 pause
