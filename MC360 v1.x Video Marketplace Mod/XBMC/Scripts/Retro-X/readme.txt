Retro-X is a feature rich Emulator/Homebrew and Python Launcher for XBMC(XBox Media Center)



FEATURES: (Version 1.01)

    * SOUND PACKS - USE YOUR OWN CUSTOM SOUNDS Create a directory under sounds with any name you like. Then copy your sounds into that directory. Must be .wav files and have the following names: move,start,end,select,launch,faves,dialog. You dont have to have a .wav for each you can just have the sounds you want like start and end. Then goto the SYSTEM CONFIG and toggle to which SOUND PACK you want. 

    * TOGGLE SHOWING ROM EXTENSIONS - CONFIGURE VIA SYSTEM CONFIG 

    * SKINNED FOR CLEARITY 

    * SKINNED FOR x-TV 

    * SKINNED FOR BLACKBOLT CLASSIC 

FEATURES: (Initial Version .99)

    * MULTIPLE LANGUAGE SUPPORT (Only English and German done but other languages can be setup easily. 

    * MULTIPLE SKIN SUPPORT (Currently MC360 and PM3 as default) (Thanks to guibuilder from Nuka1195) 

    * CONFIGURATION OF – XBOX EMULATORS 

    * CONFIGURATION OF – XBOX HOMEBREW 

    * CONFIGURATION OF – PYTHON GAMES 

    * UNLIMITED FAVOURITES TOGGLED ON/OFF. 

    * UNLIMITED SOURCES FOR EACH EMULATOR 

    * MULTIPLE SCREENSHOT/SLIDESHOW SUPPORT FOR EMULATOR PICTURES. 

    * CONFIGURABLE DISPLAY FOR SINGLE AND DUAL IMAGE DISPLAY. 

    * CONFIGURE AUTORETURN TO RETURN TO THE POINT BEFORE THE GAME WAS STARTED 

    * SEARCH SUB-DIRECTORIES. WHEN THE SEARCH SUBDIRS IS SET TO TRUE. 

    * FULLY CONFIGURABLE VIA SCRIPT NO XML EDITING REQUIRED. 

    * BACKUP ROMLISTS TO FILE FOR SUPERFAST ROM DISPLAY (After initial read) 

    * DISPLAY FAVOURITES FOR ALL EMULATORS 

!Notes:

Strings in German that need modifying : 1,2,3,86 /language/german.xml

This has been tested on the very latest builds from 2.0.1 of XBMC to Svn:7331 and works. There are a few cosmetic issues when using MC360 skin in the very latest releases of XBMC ,but apart from that it works ok.
Install:

- Simply extract the zip file and ftp over to /XBMC/script directory
Update:

- Simply overwrite the files in the Retro-X Directory. Your config.xml will not be overwritten.
Running:

When you first run the script you will be informed that no Emulators are setup so you will need to Add them through the Configuration Menu:
System Config - Menu Options:

    *
      Modify Emulator:

    Just select the Emulator to modify and all the Info will be displayed. Select OK to write changes or Cancel to revert back. 

    *
      Add Emulator:

    Emulator with Game Support:

        This is for Emulators that support loading games directly from the script. Emulators that support this function are All Xport Emus (With the exception of Mame) and Znes. There may be others and if someone knows that the Emulator they run support this then please let me know. 

    * Name - Friendly name for the Emulator you are setting up (!Required Item). 

    * Path to xbe/py - Browse to the path and select the file to run (normally default.xbe) (!Required Item) 

    * Path to Icon - Browse to the path and select the image to be displayed when viewing the Emulator. (!Required Item) 

    * Name of Source - Friendly name for the primary location of the romfiles to display. (!Required Item) 

    * Rompath - Browse to the primary location of where the roms are. (!Required Item) 

    * Romext - Extensions to look for when getting roms multiple types seperated by a space eg, 'zip nes t64' etc. (!Required Item) 

    * Picture Path - Browse to the Path where the screenshots are located. (!Optional) 

    * Picture Format - Format that the pictures are in for that Emulator. Typical examples are '%s' for all Xport Emulators or '%s.png' for Zsnes. The %s gets replaced with the rom being displayed at the time. As export stores all pictures in a Subdirectory matching the name of the rom it will display all files in the directory in a slideshow. (!Optional) 

    * Art Path - Browse to where you Artwork is located for the Emulator. (!Optional) 

    * Search Subdirs - Selecting this Toggles Searching All Subdirectories from the Initial Rompath. When enabled all subdirs are scanned for roms. The roms are all sorted alphabetically in one big list. 

    Emulator - Standalone:

        This is for Emulators that do not support passing a game directly to them. Examples of this are Mame. 

    * Name - Friendly name for the Emulator you are setting up (!Required Item). 

    * Path to xbe/py - Browse to the path and select the file to run (normally default.xbe) (!Required Item) 

    * Path to Icon - Browse to the path and select the image to be displayed when viewing the Emulator. (!Required Item) 

    HomeBrew:

        This is for setting up any Homebrew Application/Games that you would like to see on this list. 

    * Name - Friendly name for the Emulator you are setting up (!Required Item). 

    * Path to xbe/py - Browse to the path and select the file to run (normally default.xbe) (!Required Item) 

    * Path to Icon - Browse to the path and select the image to be displayed when viewing the Homebrew App/Game. (!Required Item) 

    Python Game:

        This is for setting up any Python Games. 

    * Name - Friendly name for the Emulator you are setting up (!Required Item). 

    * Path to xbe/py - Browse to the path and select the file to run (normally default.py) (!Required Item) 

    * Path to Icon - Browse to the path and select the image to be displayed when viewing the Python Game. (!Required Item) 

    *
      Delete Emulator:

    Just select the Emulator/Game/Homebrew you want to delete. You will be prompted to confirm the deletion. 

    *
      System Config:

    * Dual Display - Toggles Dual Icon Display. When enable it will display the Emualtor icon in the top wndow and the bottom display will scroll through all other images for the Rom. When False only the bottom window will be displayed in Rom view and will cycle through the Emulator icon and all other images. 

    * AutoReturn - Toggles Autoreturn Feature. When enabled it saves the current view and when you exit the game it will return to the display where the rom was launched from. This works for all configurable Emulators/Python scripts. This works best if XBMC is setup as your Dashboard. 

    * Show Rom Extensions - Toggles the display to show file extensions of the Roms being displayed. Toggles between On and Off. 

    * Select Sound - Toggles between available sound themes and Off to disable all theme sounds in script. 

Emulator Display:

The default view is to Display the Emulators/Python Games that have been configured.

Available Button Options in the Default Emulator Display are:

    * X - Display All Favourites. This searched all Emulators that have any Favourites setup and Display them in a list. 

    * B - Exit the Application. 

    * A - Select the Option. If an Item displays LAUNCH on the right hand side this indicates that the item is Emualtor-Standalone/HomeBrew or Script so will be Launched. Otherwise the roms for the selected item would be displayed. 

Rom Display:

When you selected an Emulator that has been configured with game support. A list of all available roms in the primary rompath are displayed if matching the possible extensions setup in RomExt.

Available Button Options in Rom Display View are:

    * X - Toggle Favourites on/off. Favourites are displayed at the top of the list next time you view the list. 

    * B - Go back to the Default Emulators display. 

    * A - Launch the select Rom. 

    * Y - Configure/Modify additional sources.. 

Options Available:

    * Set Default View : Select this to set the default Source to your current Source when you next view this Emulator. 

    * Add Source : This enables you to add an additional rompaths for this Emulator: 

Configuration Options:

    * Name of Source - Friendly name for the new location of the romfiles to display. (!Required Item) 

    * Rompath - Browse to the location of where the roms are. (!Required Item) 

    * Picture Path - Browse to the Path where the additional screenshots are located. If left empty will default to primary (!Optional) 

    * Art Path - Browse to the Path where the additional Artwork is located. If left empty will default to primary (!Optional) 

    * Search Subdirs - If enabled will search all Subdirectories for the new Source. 

When complete you will be prompted to show to newly created source.

    * Switch To : Switch to any of the Additional Sources available. 

    * Delete : Delete the Source Required. 

Favourites Display:

When the X button has been pressed on the default screen All Emulators will be searched for Favourites and displayed in list to select.

Available Button Options in Favourites Display View are:

    * B - Go back to the Default Emulators display. 

    * A - Launch the select Rom. 


Package Contents:
/games		(Directory)	All romlists/favourites get stored here
/language	(Directory)	Contains language files/strings.
/media		(Directory)	Non-Default images.
/skins		(Directory)	Contains MC360,Clearity,Blackbolt Classic,xTV and Default PM3 Skins.
/libs		(Directory)	Contains guibuilder.py module by Nuka1195 and core.py Config handler.
/sound		(Directory)	Contains default directory for sound themes.
default.py	(File)		Main Script.
default.tbn	(File)		ThumbNail Image/Icon for Script.
Emureturn.py	(File)		Controls Autoreturn for Python Games.


