#Wake On Lan Automatic Update and Install
#V0.01 
#pXn*Emerica
#blendz@shaw.ca
#http://www.projectxnetwork.com

#Imports
import os.path 
import re
import urllib
import xbmc
import xbmcgui
import time

#Get Script Path
ScriptPath = re.sub('^(.*?)[\\\\;]*$','\\1\\\\',os.getcwd()) #works in both emu and xbox


#Auto Update Location Information
URLsite = 'http://titancore.net/'
URLhome = URLsite + 'wakeonlan'+'/'


ACTION_MOVE_LEFT        =  1    
ACTION_MOVE_RIGHT       =  2
ACTION_MOVE_UP          =  3
ACTION_MOVE_DOWN        =  4
ACTION_PAGE_UP          =  5 
ACTION_PAGE_DOWN        =  6 
ACTION_SELECT_ITEM      =  7 
ACTION_HIGHLIGHT_ITEM   =  8 
ACTION_PARENT_DIR       =  9 
ACTION_PREVIOUS_MENU    = 10 
ACTION_SHOW_INFO        = 11
ACTION_PAUSE            = 12
ACTION_STOP             = 13
ACTION_NEXT_ITEM        = 14
ACTION_PREV_ITEM        = 15
ACTION_XBUTTON			= 18 

	
class installer(xbmcgui.Window): 
	def __init__(self):
		urllib.urlcleanup()
		dialog = xbmcgui.DialogProgress()
		err = xbmcgui.Dialog()
		dialog.create("Wake on Lan Installer", "Contacting Update Server", "Please wait....")
		if not dialog.iscanceled(): 
			try:
				dialog.update(10)
				urllib.urlretrieve(URLhome+'background.png',ScriptPath+'background.png')
				dialog.update(25)
				urllib.urlretrieve(URLhome+'settings.xml',ScriptPath+'settings.xml')
				dialog.update(50)
				urllib.urlretrieve(URLhome+'wol.txt',ScriptPath+'wol.py')
				dialog.update(75)
				urllib.urlretrieve(URLhome+'settingsmgr.txt',ScriptPath+'settingsmgr.py')
				dialog.update(100)
				k=err.ok("Installtion Complete", "This auto update will be replaced with the latest version each time you run wol.py", "Thanks for using Wake on Lan")
			except:
				k=err.ok("Wake on Lan Installer","Master Server Connection Problems", "Please try again later.")
				pass
		dialog.close()
		installer.close()

W = installer()
W.doModal()