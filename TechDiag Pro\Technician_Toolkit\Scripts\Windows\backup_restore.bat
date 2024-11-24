@echo off
echo Backup and Restore Script

:: Backup Example
echo Backing up Documents...
xcopy C:\Users\%USERNAME%\Documents E:\Backup\Documents /E /H /C /I

:: Restore Example
echo Restoring Documents...
xcopy E:\Backup\Documents C:\Users\%USERNAME%\Documents /E /H /C /I

echo Backup and Restore operations completed.
pause