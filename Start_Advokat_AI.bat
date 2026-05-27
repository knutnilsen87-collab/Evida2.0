@echo off
setlocal

set "ROOT=%~dp0"
set "LAUNCHER=%ROOT%scripts\start-dev.ps1"

if not exist "%LAUNCHER%" (
  echo Fant ikke startscriptet:
  echo %LAUNCHER%
  echo.
  pause
  exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -File "%LAUNCHER%"
