@echo off
if exist build rmdir /s /q build
pyinstaller --clean --onefile --windowed --icon=pirarara.ico --name pirarara ..\src\pirarara\main.py
if exist build rmdir /s /q build
if exist dist move dist\*.exe .
if exist dist rmdir dist
:END
