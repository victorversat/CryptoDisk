@echo off
echo Requesting administrator privileges...
if not "%1"=="am_admin" (powershell start -verb runas '%0' am_admin & exit /b)

cd /d "%~dp0"
echo Installing CryptoDisk with administrator privileges...
python working_installer.py
echo.
echo Press any key to close...
pause >nul