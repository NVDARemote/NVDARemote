@echo off
del /s /q addon\manifest.ini>NUL
del /s /q "remote-1.2.nvda-addon">NUL
call scons -s
"remote-1.3.nvda-addon"