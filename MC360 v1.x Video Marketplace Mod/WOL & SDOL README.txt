MC360 Remote Computer Startup/Shutdown Mod for v1.0 (works with newer versions as well...and the xml files this changes aren't likely to change in the official build any time soon.)

If you have any problems with this script, feel free to post in the thread, or PM on xbox-scene, as screen name timdog82001

HOW TO SET UP SCRIPTS:



Note: This may look like a lot of words, and may seem complicated because of that, but this is only because I made sure to write down every detail of every step so there would be absolutely NO ONE wondering how to get this working on their computer/xbox. It is actually very easy and very self expanatory, and most should be able to figure it out WITHOUT this guide, but it's here for the less computer literate. There are only a few things I can think of that aren't completely obvious:

1. Make sure not to run the SETUP.EXE or SETUP1.EXE files to try to install the sol.exe for the shutdown on lan. It isn't necessary, and they don't work.

2. You have to manually edit the settings.ini and sol.py to make sure they match eachother and match the settings of your computer.

3. You have to enable Wake On Lan in your computers BIOS. Look in your computer's or motherboard's manual for more info.


All this and much more is covered in more depth below.


IDIOT'S GUIDE TO CONFIGURING SCRIPTS (just kidding about the idiot part ;):


Shutdown On Lan (SOL/SDOL):

For this script, you will have to run a tiny program in the background on your computer to listen for your xbox telling it to shutdown. You can easily add it to the Startup folder, so it will start with your computer. Open up the folder "ShutdownPConLAN" and right click on the file "ShutdownOnLAN.rar" and choose "Extract to ShutdownOnLan\." Navigate into the newly created folder and right click on "sol.CAB" and click on "Extract to sol\." Now, in this newly created folder, open settings.ini with a text editor, like notepad. Now, navigate to the root of your ShutdownPConLan folder and open the sol.py file with a text editor. (don't bother with the sol.py file found next to the settings.ini file, because the xbox won't know to look there). Now, just make sure the serverPorts match and change the IP address in sol.py to match that of your computer. To figure out the IP Address of your computer, go Start -> Run and type CMD and press enter. A black window will appear, in which you should type "ipconfig" and press enter. A few numbers should pop up, one of which will say "IP Address" next to it. Simply replace the "ServerHostName" number in the sol.py file with the the IP Address of your computer. Now, close both files, making sure to save.

Now, transfer the whole ShutdownPConLan folder into the root of your scripts folder in XBMC on your xbox, and double click on the sol.exe file found in the folder where you edited the settings.ini file. A small icon of a door should appear in your taskbar (bottom right corner of your computer screen). You should now be able to shutdown your computer by running this script on your xbox.

NOTE: You may have to open a port in your firewall(s) before this will work.
NOTE: Also, don't try running the SETUP.exe or SETUP1.exe. They just don't work.

If you would like this program to run everytime you start up the computer, rightclick on sol.exe, and select "Create Shortcut." Now, just move this file into your startup folder. This can easily be accessed by going Start -> All Programs, and right click on "Startup" and choose "open." Simply move the shortcut here (make sure not to move the actual sol.exe, or it will not work).


Wake On Lan (WOL):

To configure the Wake on Lan to work, you need to first, make sure your computer has this capability (most newer ones do, I believe) and you need to enable it, by going into your computer BIOS and enabling an option that is frequently labeled OnBoard LAN or Boot from LAN. It may be found in the ‘OnBoard Device Configuration’, ‘Boot’, or ‘PowerSave’ menu, but it all depends on the BIOS. In case of doubt, consult the documentation for your motherboard or computer. To access your computer BIOS, this is normally done by hitting delete or F4 or ESC or something similar repeatedly while the computer is first starting up. If you look in your user manual for your motherboard, or for your computer if its a dell or something like that, you should be able to figure it out. Google or the manufacturers website might be useful for figuring this out if you can't find it in the manual. Once you have it properly enabled, I believe the lights on your network port should stay lit when plugged in, even if the computer is shut down.

Now that you've enabled it in the BIOS of your computer, all you should have to do is configure it on your xbox. On your computer, go Start -> Run and type "cmd" and press enter. A black window should pop up, and here type "ipconfig /all" and press enter. Your active network ports should all pop up here with the mac address(es) (should be in a format similar to "00-17-31-8B-2E-1C." If there's more than one, figure out which one is connected to the network your xbox is on. Now, on the xbox, start the script, and go to "Change Settings." Here, you can add up to 5 different computers, and name each one. Go to Computer 1, change the name if you'd like, and change the mac address to the one you found on your computer. Now, when you shutdown your computer, if everything is configured correctly, you should be able to start your computer with a couple easy clicks of a button on your xbox.

NOTE: There is an "autoupdate.py" included with this script. Don't run it, it will only break the script and make it nonfunctional.