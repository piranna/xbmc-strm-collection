@echo off
ECHO ------------------------------
ECHO Creating "XBMC-TV" Folder
rmdir XBMC-TV /S /Q

ECHO ------------------------------
ECHO Building XBMC-TV Directory...
xcopy "Andorra" "XBMC-TV\Andorra" /E /Q /I /Y
xcopy "Antigua and Barbados" "XBMC-TV\Antigua and Barbados" /E /Q /I /Y
xcopy "Argentina" "XBMC-TV\Argentina" /E /Q /I /Y
xcopy "Armenia" "XBMC-TV\Armenia" /E /Q /I /Y
xcopy "Austria" "XBMC-TV\Austria" /E /Q /I /Y
xcopy "Australia" "XBMC-TV\Australia" /E /Q /I /Y
xcopy "Belgium" "XBMC-TV\Belgium" /E /Q /I /Y
xcopy "Brazil" "XBMC-TV\Brazil" /E /Q /I /Y
xcopy "Canada" "XBMC-TV\Canada" /E /Q /I /Y
xcopy "Chile" "XBMC-TV\Chile" /E /Q /I /Y
xcopy "China" "XBMC-TV\China" /E /Q /I /Y
xcopy "Colombia" "XBMC-TV\Colombia" /E /Q /I /Y
xcopy "Cuba" "XBMC-TV\Cuba" /E /Q /I /Y
xcopy "Czech Republic" "XBMC-TV\Czech Republic" /E /Q /I /Y
xcopy "Denmark" "XBMC-TV\Denmark" /E /Q /I /Y
xcopy "Dominican Republic" "XBMC-TV\Dominican Republic" /E /Q /I /Y
xcopy "El Salvador" "XBMC-TV\El Salvador" /E /Q /I /Y
xcopy "Estonia" "XBMC-TV\Estonia" /E /Q /I /Y
xcopy "France" "XBMC-TV\France" /E /Q /I /Y
xcopy "Germany" "XBMC-TV\Germany" /E /Q /I /Y
xcopy "Greece" "XBMC-TV\Greece" /E /Q /I /Y
xcopy "Haiti" "XBMC-TV\Haiti" /E /Q /I /Y
xcopy "Honduras" "XBMC-TV\Honduras" /E /Q /I /Y
xcopy "Hungary" "XBMC-TV\Hungary" /E /Q /I /Y
xcopy "India" "XBMC-TV\India" /E /Q /I /Y
xcopy "Israel" "XBMC-TV\Israel" /E /Q /I /Y
xcopy "Italy" "XBMC-TV\Italy" /E /Q /I /Y
xcopy "Japan" "XBMC-TV\Japan" /E /Q /I /Y
xcopy "Korea" "XBMC-TV\Korea" /E /Q /I /Y
xcopy "Latvia" "XBMC-TV\Latvia" /E /Q /I /Y
xcopy "Lithuania" "XBMC-TV\Lithuania" /E /Q /I /Y
xcopy "Luxembourg" "XBMC-TV\Luxembourg" /E /Q /I /Y
xcopy "Malaysia" "XBMC-TV\Malaysia" /E /Q /I /Y
xcopy "Malta" "XBMC-TV\Malta" /E /Q /I /Y
xcopy "Mexico" "XBMC-TV\Mexico" /E /Q /I /Y
xcopy "Netherlands" "XBMC-TV\Netherlands" /E /Q /I /Y
xcopy "Panama" "XBMC-TV\Panama" /E /Q /I /Y
xcopy "Poland" "XBMC-TV\Poland" /E /Q /I /Y
xcopy "Portugal" "XBMC-TV\Portugal" /E /Q /I /Y
xcopy "Romania" "XBMC-TV\Romania" /E /Q /I /Y
xcopy "Russia" "XBMC-TV\Russia" /E /Q /I /Y
xcopy "Slovakia" "XBMC-TV\Slovakia" /E /Q /I /Y
xcopy "Slovenia" "XBMC-TV\Slovenia" /E /Q /I /Y
xcopy "Spain" "XBMC-TV\Spain" /E /Q /I /Y
xcopy "Sri Lanka" "XBMC-TV\Sri Lanka" /E /Q /I /Y
xcopy "Sweden" "XBMC-TV\Sweden" /E /Q /I /Y
xcopy "Switzerland" "XBMC-TV\Switzerland" /E /Q /I /Y
xcopy "Thailand" "XBMC-TV\Thailand" /E /Q /I /Y
xcopy "Turkey" "XBMC-TV\Turkey" /E /Q /I /Y
xcopy "Ukraine" "XBMC-TV\Ukraine" /E /Q /I /Y
xcopy "United Kingdom" "XBMC-TV\United Kingdom" /E /Q /I /Y
xcopy "United States" "XBMC-TV\United States" /E /Q /I /Y
xcopy "Venezuela" "XBMC-TV\Venezuela" /E /Q /I /Y
xcopy "Vietnam" "XBMC-TV\Vietnam" /E /Q /I /Y
xcopy "Webcams" "XBMC-TV\Webcams" /E /Q /I /Y

ECHO ------------------------------
ECHO Removing SVN directories from XBMC-TV...
FOR /R XBMC-TV %%d IN (SVN) DO @RD /S /Q "%%d" 2>NUL

ECHO Complete
ECHO ftp the "XBMC-TV" folder to your xbox.
ECHO Happy Watching!

pause