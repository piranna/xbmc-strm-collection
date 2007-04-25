# Switch splash.png script by Asteron 
# v1.0 - 2007/02/21 
# http://asteron.projects.googlepages.com/

import os, shutil, traceback
import xbmc, xbmcgui

def main():
	keymapfile = 'Q:\\UserData\\keymap.xml'
	skinname = xbmc.getSkinDir()
	trimmedname = ''.join(skinname.lower().split())
	customkeymap = 'Q:\\skin\\' + skinname + '\\extras\\keymap.xml'
	keymapbackup = 'Q:\\UserData\\keymap.xml.'+trimmedname
	if not os.path.exists(customkeymap):
		xbmcgui.Dialog().ok('ERROR', 'Custom keympap.xml not found', customkeymap)
		return
	
	if os.path.exists(keymapbackup):
		os.remove(keymapfile)
		shutil.move(keymapbackup, keymapfile)
		xbmc.executebuiltin('Skin.SetBool(customKeymap)')
		xbmc.executebuiltin('Skin.ToggleSetting(customKeymap)') #make sure its off		
	else:
		shutil.move(keymapfile, keymapbackup)
		shutil.copy(customkeymap, keymapfile)
		xbmc.executebuiltin('Skin.SetBool(customKeymap)')		
try:
	main()
except:
	traceback.print_exc()
