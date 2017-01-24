@echo off
cl /WX /Ox /nologo addon\globalPlugins\remoteClient\url_handler.cpp user32.lib /EHsc /link /subsystem:windows
move url_handler.exe addon\globalPlugins\remoteClient\ > NUL
