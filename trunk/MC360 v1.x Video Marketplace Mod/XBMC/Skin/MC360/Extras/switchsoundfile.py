# Switch splash startup sound file script by Asteron 
# v1.0 - 2007/02/21 
# http://asteron.projects.googlepages.com/

import os, shutil, traceback
import xbmc, xbmcgui

def main():
	soundfile = 'Q:\\skin\\MC360\\sounds\\mc360_startup.wav'
	skinname = xbmc.getSkinDir()
	trimmedname = ''.join(skinname.lower().split())
	customsoundfile = 'Q:\\skin\\' + skinname + '\\extras\\mc360_startup.wav'
	soundfilebackup = 'Q:\\skin\\' + skinname + '\\extras\\mc360_startup.wav'+trimmedname
	if not os.path.exists(customsoundfile):
		xbmcgui.Dialog().ok('ERROR', 'Custom sound file not found', customsoundfile)
		return
	
	if os.path.exists(soundfilebackup):
		os.remove(soundfile)
		shutil.move(soundfilebackup, soundfile)
		xbmc.executebuiltin('Skin.SetBool(CustomStartupSound)')
		xbmc.executebuiltin('Skin.ToggleSetting(CustomStartupSound)') #make sure its off		
	else:
		shutil.move(soundfile, soundfilebackup)
		shutil.copy(customsoundfile, soundfile)
		xbmc.executebuiltin('Skin.SetBool(CustomStartupSound)')		
try:
	main()
except:
	traceback.print_exc()
