@echo off
ECHO ------------------------------
ECHO Creating "XBMC-TV" Folder
rmdir XBMC-TV /S /Q

ECHO ------------------------------
ECHO Building XBMC-TV Directory...
xcopy "Andorra" "XBMC-TV\Andorra" /E /Q /I /Y
xcopy "Armenia" "XBMC-TV\Armenia" /E /Q /I /Y
xcopy "Austria" "XBMC-TV\Austria" /E /Q /I /Y
xcopy "Australia" "XBMC-TV\Australia" /E /Q /I /Y
xcopy "Brazil" "XBMC-TV\Brazil" /E /Q /I /Y
xcopy "Canada" "XBMC-TV\Canada" /E /Q /I /Y
xcopy "Czech Republic" "XBMC-TV\Czech Republic" /E /Q /I /Y
xcopy "Denmark" "XBMC-TV\Denmark" /E /Q /I /Y
xcopy "Estonia" "XBMC-TV\Estonia" /E /Q /I /Y
xcopy "France" "XBMC-TV\France" /E /Q /I /Y
xcopy "Germany" "XBMC-TV\Germany" /E /Q /I /Y
xcopy "Hungary" "XBMC-TV\Hungary" /E /Q /I /Y
xcopy "Italy" "XBMC-TV\Italy" /E /Q /I /Y
xcopy "Latvia" "XBMC-TV\Latvia" /E /Q /I /Y
xcopy "Lithuania" "XBMC-TV\Lithuania" /E /Q /I /Y
xcopy "Japan" "XBMC-TV\Japan" /E /Q /I /Y
xcopy "Luxembourg" "XBMC-TV\Luxembourg" /E /Q /I /Y
xcopy "Netherlands" "XBMC-TV\Netherlands" /E /Q /I /Y
xcopy "Poland" "XBMC-TV\Poland" /E /Q /I /Y
xcopy "Portugal" "XBMC-TV\Portugal" /E /Q /I /Y
xcopy "Romania" "XBMC-TV\Romania" /E /Q /I /Y
xcopy "Russia" "XBMC-TV\Russia" /E /Q /I /Y
xcopy "Slovakia" "XBMC-TV\Slovakia" /E /Q /I /Y
xcopy "Slovenia" "XBMC-TV\Slovenia" /E /Q /I /Y
xcopy "Sweden" "XBMC-TV\Sweden" /E /Q /I /Y
xcopy "Switzerland" "XBMC-TV\Switzerland" /E /Q /I /Y
xcopy "United Kingdom" "XBMC-TV\United Kingdom" /E /Q /I /Y
xcopy "United States" "XBMC-TV\United States" /E /Q /I /Y
xcopy "Webcams" "XBMC-TV\Webcams" /E /Q /I /Y

ECHO ------------------------------
ECHO Removing SVN directories from XBMC-TV...
FOR /R XBMC-TV %%d IN (SVN) DO @RD /S /Q "%%d" 2>NUL

ECHO Complete
ECHO ftp the "XBMC-TV" folder to your xbox.
ECHO Happy Watching!

pause