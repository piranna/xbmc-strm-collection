MC360 monster mod by timdog82001

1.  XBMC Video Marketplace / Script  Marketplace
        
         -  a centralized spot where you can easily and elegantly access all media related scripts and video files, including Streaming TV packs.  Each button currently has 3 selectable categories: Single Script mode, Bookmark Mode, and Category Script Mode.  Single script mode allows you to launch a script directly from that button, bookmark mode opens up the video bookmark you specify in the settings, and category mode will open a dialog with other scripts to choose from.  This is so you can make the button say "Podcasts" or something, add the icon of your choice, and in the dialog you would add all your podcast related scripts.  This allows you to have your scripts navigable in a clean, organized manner, while still keeping them in the root of your scripts folder, where they need to be if you are to link to them from skins.  Completely customizable, even down to an option to rename the marketplace to your choosing and/or move it to the games blade. (for those of you who are interested in using this more as a "Script marketplace" or something similar, somewhat similar to the script favorites menu, but configurable in skin, and categorizable.  The marketplace is also great for wives, children, or girlfriends who can't easily navigate throughout the whole skin.  You can link to everything they'll ever need in one spot.  I'll probably be adding support for audio and picture bookmarks too.

2.  XBMC-TV - Your source for Broadband (200k+) LIVE video streams on XBMC

        -  Included as part of the Marketplace mod, XBMC-TV is a team project led by Akaigotchi to bring the first truly reliable Stream Pack to XBMC.  Although still very young, it already has about 500 stations, and there are entire "genres" of Streaming Video we haven't yet started attacking.  It is all separated up by country, and is automatically checked for nonfunctional streams which are promptly removed, so there is no worry of running into non-functional video streams (assuming you have the most recent version).  It currently is simply a pack of .strm files, but in the future will be evolving into a full blown script.  For more information on XBMC-TV, see the threads either here http://forums.xbox-scene.com/index.php?showtopic=582032 or on the official xboxmediacenter forums http://www.xboxmediacenter.com/forum/showthread.php?t=24486.  Updates are available via SVN (you can find information on that in the links above) or in a weekly snapshot uploaded every monday, available here: http://www.xbmc-tv.com/   Check it out!

3.  Separate TV Shows / Movies buttons on media blade

        -  adds the option to link directly to your movies and TV show folders directly from the media home blade.

4.  Retro-X  Script Integration

        -  changes "Xbox Arcade" button in Games blade to launch the Retro-X script instead of going to your emulator folder.  (for those who don't know, Retro-X is a python script by chunk_1970 which allows you to launch all your emulator and python games from one spot. See original thread here: http://forums.xbox-scene.com/index.php?showtopic=519798)

5.  Remote Computer Startup/Shutdown (WOL/SOL)

        -  Allows you to remotely start up or shutdown your personal computer over the network using your xbox and the sol and wol scripts, included in mod, as are all other scripts mentioned.  Everything needed is included, but refer to thread here for instructions on how to get that working, or read the readme.txt include here.  Requires a little fidgeting with settings on your computer.  http://forums.xbox-scene.com/index.php?showtopic=587192

6.  Media Center Extender mod

        -  Adds a button to the Media Blade which launches the Media Center Extender, allowing users of the Xbox Media Center Extender and Windows XP Media Center Edition to link to their computer like the actual 360, where they can stream video files, pictures and so on, and also, schedule and view recordings on live TV (which is obviously where the real advantage lies).  Though previously required some minor XML editing, this mod is now fully configured in-skin.  Though no longer completely acurrate, you can find the original thread here: http://forums.xbox-scene.com/index.php?showtopic=587425

For a slightly more expansive explanation of all features, please go to the original release thread, found here:

http://forums.xbox-scene.com/index.php?act=ST&f=193&t=593354


Here are some basic instructions for installation of this mod.  There will be readme's included as well, and I suggest looking at the original thread for the remote computer startup/shutdown mod for instructions if you plan on using that.  

INSTRUCTIONS: 

1.  FTP into your xbox and find the XBMC folder on your xbox.  Copy the XBMC folder found in this mod over the XBMC folder on the xbox. Note: no parts of XBMC itself are modified, this is simply so you can transfer all scripts and everything with one step.  If there are any scripts included with this mod that you already have on your xbox and would rather just keep the version you have, simply delete them from the mod before transfering over.

2.  FTP the "Marketplace Icons" and "XBMC-TV" folders to somewhere convenient on your xbox hard drive.  I simply placed mine in the root of my E drive.


3.  Make sure everything copied properly, and restart XBMC.

4.  Once XBMC restarts, go into Videos and select "Add Source."  Navigate to the XBMC-TV folder and select OK.  Make sure the Bookmark is named XBMC-TV and select "done."  Note: this is needed for the Video Marketplace default settings, otherwise one of the buttons will be broken.

5.  Go to the MC360 Guide by pressing Start on the controller or selecting the MC360 Guide button with the remote control.  Go to "Personal Settings" and then "Skin Mods Settings."  Configure things as you like.  Things are fairly self explanatory.  MCE stands for Media Center Extender.  WOL/SOL stands for Wake-On-LAN and Shutdown-On-LAN and enables the button to remotely start and shutdown your computer.


Movie / TV Show Button Instructions:

1.  Create 2 bookmarks that separately link to your TV Shows and Movies

2.  Enable option in Skin Mods Settings.

3.  Link buttons to appropriate Bookmarks by type in the name of the corresponding bookmark in the "Link to Movie/TV Show Bookmark" buttons.

Media Center Extender Instructions:

1.  Make sure you have Media Center Extender for Xbox installed in your xbox hard driveor in the DVD drive.

2.  Enable option "Enable MCE Button" in Skin Mods Settings.

3.  Select button "Specify Media Center folder..." and navigate to your Xbox Media Center Extender folder (probably named Media Center Extender for Xbox).  Select "done" and exit window.

4.  Navigate to Media Blade and select Media Center to launch program.


For further instructions for both the Media Center button and the Remote Computer start/shutdown, please see appropriate readme's included with mod.


FUTURE POSSIBILITIES?


Let me know what you guys think about these features being added in the future.  Any other features you would like?  Assuming anybody even wants this mod in the first place haha


- Add bookmarks to category scripts dialogs


- Add ability to use library mode with bookmarks


- Add option to link TV Shows and Movies to scripts and to have custom names


- Clean up Skin Mods Settings window


- Make custom square image icon thing for marketplace.  I have almost no experience with Illustrator.  If someone wants to whip up a custom icon for the Video Marketplace and it looks good, I'd be happy to include it in place of the eX button, since that's somewhat redundant, already found in the XBMC Live Place.


- Evolve into more of a "Media Marketplace" and add options for music or picture bookmarks


- Add names of current script in catalog config dialog


- Ability to automatically look in multiple places for XBMC-TV folder (probably root of E and F drives) and default to looking for bookmark if its not located in either of those places.  Not sure if this is possible however, but if anybody knows how, let me know!

- Fix Launch Browser script to replace current "News Videos" button with "Music Videos" to replicate the actual 360 setup.  Not sure how likely this is to happen, since I know hardly anything about python...

- Skin all default scripts to match mc360 better?


KNOWN BUGS: 

- Video preview doesn't fade with window changes.  Not sure if this is fixable, since it does it in the video playlist window too...

- Some textures randomly disappear when watching certain video files.  Help?  Not sure how to fix this.
