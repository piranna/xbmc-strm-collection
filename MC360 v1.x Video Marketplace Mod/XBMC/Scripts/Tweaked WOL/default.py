#Imports
import os.path 
import re
import urllib
import xbmc
import xbmcgui
import time
import settingsmgr
import socket
import struct

ScriptPath = re.sub('^(.*?)[\\\\;]*$','\\1\\\\',os.getcwd()) #works in both emu and xbox
settingsfile=ScriptPath+'settings.xml'
settings=settingsmgr.ReadSettings(settingsfile)

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

def wake_on_lan(macaddress):
    if len(macaddress) == 12:
        pass
    elif len(macaddress) == 12 + 5:
        sep = macaddress[2]
        macaddress = macaddress.replace(sep, '')
    else:
        raise ValueError('Incorrect MAC address format')
 
    # Pad the synchronization stream.
    data = ''.join(['FFFFFFFFFFFF', macaddress * 20])
    send_data = '' 

    # Split up the hex values and pack.
    for i in range(0, len(data), 2):
        send_data = ''.join([send_data,
                             struct.pack('B', int(data[i: i + 2], 16))])

    # Broadcast it to the LAN.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(send_data, ('<broadcast>', 7))


class WoL(xbmcgui.Window): 
	def __init__(self):
		dialog=xbmcgui.Dialog()
		try:
			urllib.urlcleanup()
			# urllib.urlretrieve(URLhome+'autoupdate.txt',ScriptPath+'autoupdate.py')
		except: 
			dialog.ok("Wake on Lan Installer","Master Server Connection Problems", "Please try again later.")
		pass
		#dialog.close()


		options=['Start Timothys Computer','Wake On Lan 2','Wake On Lan 3','Wake On Lan 4', 'Wake On Lan 5', 'Change Settings','Exit Wake On Lan']
		choice=dialog.select("PC Network...",options)
		if choice==6:
			xbmcgui.Window.close()
		if choice==5:
			settingsmgr.OpenControlPanel(settingsfile)
			WoL()
		if choice==4:
			dialog = xbmcgui.Dialog()
			confirm=dialog.yesno('Wake On Lan', "Do you want to wake this pc?", "Mac: "+settings['mac5'], "Name: "+settings['mac5name'])
			if confirm:
				wake_on_lan(settings['mac5'])
				WoL()
			else:
				WoL()
			
		if choice==3:
			dialog = xbmcgui.Dialog()
			confirm=dialog.yesno('Wake On Lan', "Do you want to wake this pc?", "Mac: "+settings['mac4'], "Name: "+settings['mac4name'])
			if confirm:
				wake_on_lan(settings['mac4'])
				WoL()
			else:
				WoL()
		if choice==2:
			dialog = xbmcgui.Dialog()
			confirm=dialog.yesno('Wake On Lan', "Do you want to wake this pc?", "Mac: "+settings['mac3'], "Name: "+settings['mac3name'])
			if confirm:
				wake_on_lan(settings['mac3'])
				WoL()
			else:
				WoL()
		if choice==1:
			dialog = xbmcgui.Dialog()
			confirm=dialog.yesno('Wake On Lan', "Do you want to wake this pc?", "Mac: "+settings['mac2'], "Name: "+settings['mac2name'])
			if confirm:
				wake_on_lan(settings['mac2'])
				WoL()
			else:
				WoL()
		if choice==0:
			dialog = xbmcgui.Dialog()
			confirm=dialog.yesno('Wake On Lan', "Do you want to wake this pc?", "Mac: "+settings['mac1'], "Name: "+settings['mac1name'])
			if confirm:
				wake_on_lan(settings['mac1'])
				WoL()
			else:
				WoL()
		dialog.close()

W = WoL()
W.doModal()

