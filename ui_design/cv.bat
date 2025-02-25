@echo off
set SCRIPT_PATH=%~dp0

if not exist ..\.venv\ goto :END
if not exist ..\.venv\Lib\site-packages\PySide6\uic.exe goto :END
for /f "usebackq delims==" %%A in (`dir /s /b ..\.venv\Lib\site-packages\PySide6\uic.exe`) do (
    set UIC_TOOL=%%A
)

if not exist ..\src\pirarara\gui\dialogs goto :END
pushd ..\src\pirarara\gui\dialogs
set COPY_PATH=%CD%
popd

:MAIN
echo TOOL=[%UIC_TOOL%]
echo COPY_PATH=[%COPY_PATH%]

rem カレントフォルダにあるフォルダ内から処理する
for /f "usebackq delims==" %%A in (`dir /ad /on /b`) do (
    call :CV_IN_DIR "%%A"
)

goto :END
if not exist *.ui goto goto :END
for /f "usebackq delims==" %%B in (`dir /b /on *.ui`) do (
    echo call :UI_2_PY "%%B" %COPY_PATH%
    rem call :UI_2_PY "%%B" %COPY_PATH%
)

goto :END

:CV_IN_DIR
    set DIRNAME=%~1

    pushd %DIRNAME%
        if not exist *.ui goto :NO_UI
        for /f "usebackq delims==" %%B in (`dir /b /on *.ui`) do (
            if not exist %COPY_PATH%\%DIRNAME%\ mkdir %COPY_PATH%\%DIRNAME%
            echo call :UI_2_PY %%B %COPY_PATH%\%DIRNAME%
            call :UI_2_PY %%B %COPY_PATH%\%DIRNAME%
        )
    :NO_UI
    popd

    exit /b

:UI_2_PY
    set IN_FILE=%~1
    set OUT_FILE=%~n1_ui.py

    if exist %OUT_FILE% del %OUT_FILE%
    echo %UIC_TOOL% -g python %IN_FILE% -o %OUT_FILE%
    %UIC_TOOL% -g python %IN_FILE% -o %OUT_FILE%
rem    echo if exist %OUT_FILE% move %OUT_FILE% %2>nul
rem    if exist %OUT_FILE% move %OUT_FILE% %2>nul
    exit /b

:END
