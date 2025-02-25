@echo off
set SCRIPT_PATH=%~dp0
pushd %SCRIPT_PATH%
cd ..
if not exist .venv\ goto :END
if not exist .venv\Lib\site-packages\PySide6\designer.exe goto :END
.venv\Lib\site-packages\PySide6\designer.exe

:END
popd
