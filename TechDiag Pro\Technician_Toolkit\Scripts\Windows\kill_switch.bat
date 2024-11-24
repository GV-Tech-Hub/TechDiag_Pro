@echo off
echo Initiating Kill Switch...
echo Terminating non-essential applications...

:: List of non-essential processes to kill
taskkill /F /IM notepad.exe
taskkill /F /IM chrome.exe
taskkill /F /IM firefox.exe
taskkill /F /IM spotify.exe

echo Kill Switch executed successfully.
pause