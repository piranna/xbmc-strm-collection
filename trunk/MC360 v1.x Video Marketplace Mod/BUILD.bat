@echo off
ECHO ------------------------------
ECHO Creating "BUILD" Folder
rmdir BUILD /S /Q

ECHO ------------------------------
ECHO Please enter your build option 

ECHO (1) Build with Widescreen Icons
ECHO (2) Build with Standard Wide Icons

SET /p SELECTION=Enter the number of your build option and press enter:

IF "%SELECTION%"=="1" GOTO WIDE_ICONS
IF "%SELECTION%"=="2" GOTO BIG_ICONS

:WIDE_ICONS
ECHO ------------------------------
ECHO Building with Wide Icons
ECHO ------------------------------

ECHO Copying content..
xcopy "Wide Marketplace Icons" "BUILD\Marketplace Icons" /E /Q /I /Y
GOTO MAIN


:BIG_ICONS
ECHO ------------------------------
ECHO Building with Big Icons
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








