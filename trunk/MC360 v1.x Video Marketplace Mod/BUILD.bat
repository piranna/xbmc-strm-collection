@echo off
ECHO ------------------------------
ECHO Creating "BUILD" Folder
rmdir BUILD /S /Q

ECHO ------------------------------
ECHO Please enter your build option 

ECHO (1) Build with Widescreen Icons
ECHO (2) Build with Standard Wide Icons

SET /p SELECTION=Enter the number of your build option and press enter:

IF "%SELECTION%"=="1" GOTO WIDESCREEN_ICONS
IF "%SELECTION%"=="2" GOTO STANDARD_ICONS

:WIDESCREEN_ICONS
ECHO ------------------------------
ECHO Building with Widescreen Icons
ECHO ------------------------------

ECHO Copying content..
xcopy "Wide Marketplace Icons" "BUILD\Marketplace Icons" /E /Q /I /Y
GOTO MAIN


:STANDARD_ICONS
ECHO ------------------------------
ECHO Building with Standard Wide Icons
ECHO ------------------------------

ECHO Copying content..

xcopy "Marketplace Icons" "BUILD\Marketplace Icons" /E /Q /I /Y
GOTO MAIN


:MAIN
xcopy "XBMC" "BUILD\XBMC" /E /Q /I /Y
GOTO CLEANUP


:CLEANUP
ECHO ------------------------------
ECHO Removing SVN directories from BUILD...
FOR /R BUILD %%d IN (SVN) DO @RD /S /Q "%%d" 2>NUL

ECHO Complete
pause








