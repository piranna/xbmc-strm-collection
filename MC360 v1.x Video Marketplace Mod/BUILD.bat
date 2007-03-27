@echo off
ECHO ------------------------------
ECHO Creating "BUILD" Folder
rmdir BUILD /S /Q

ECHO ------------------------------
ECHO Building XBMC-TV Directory...
xcopy "Marketplace Icons" "BUILD\Marketplace Icons" /E /Q /I /Y
xcopy "XBMC" "BUILD\XBMC" /E /Q /I /Y

ECHO ------------------------------
ECHO Removing SVN directories from BUILD...
FOR /R BUILD %%d IN (SVN) DO @RD /S /Q "%%d" 2>NUL

ECHO Complete


pause