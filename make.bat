@echo off
del /s /q addon\manifest.ini>NUL
del /s /q "remote-1.01.nvda-addon">NUL
call scons -s
"remote-1.01.nvda-addon"