@echo off
setlocal
cd /d "%~dp0"

set "LAUNCHER=%~dp0scripts\start-dev.ps1"

if exist "%LAUNCHER%" goto run_launcher
echo Fant ikke startscriptet:
echo "%LAUNCHER%"
echo.
pause
exit /b 1

:run_launcher
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%LAUNCHER%"
if not errorlevel 1 goto done
echo.
echo Start feilet. Se meldingen over.
pause
exit /b 1

:done
