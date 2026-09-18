@echo off
cd /d D:\mysite\blogtoolsboot
start http://localhost:1314
.\hugo.exe server -D
pause
