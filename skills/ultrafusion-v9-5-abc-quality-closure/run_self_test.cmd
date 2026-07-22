@echo off
python "%~dp0scripts\self_test.py"
exit /b %errorlevel%
