'''
    textwindow.py - Simple window for displaying long texts

    Version changelog:
        0.1 (13 may 2006):
            First version
    
    The dialog was copied from the Aftonbladet XBMC script created by Anders Willstedt and can
    be downloaded fully from www.xbmcscripts.com.
'''
import os, xbmc, xbmcgui, rss, sys
import xml.dom.minidom, urllib, os, os.path, string, traceback, time

try: Emulating = xbmcgui.Emulating
except: Emulating = False

ACTION_SELECT_ITEM      = 7
ACTION_PREVIOUS_MENU    = 10

if Emulating: PATH_ROOT = os.getcwd() + "/"
else: PATH_ROOT = "Q:\\scripts\\GameTrailersRssReader\\"
if Emulating: PATH_IMAGE = PATH_ROOT + "../img/"
else: PATH_IMAGE = PATH_ROOT + "img\\"

class Dialog(xbmcgui.WindowDialog):
    def __init__(self):
        if Emulating: xbmcgui.Window.__init__(self)
        self.setCoordinateResolution(6) # scales objects automatically
        
        imageWidth = 400
        imageHeight = 300
        
        xPos = (self.getWidth() - imageWidth) / 2
        yPos = (self.getHeight() - 300) / 2
        
        self.imgBackground = xbmcgui.ControlImage(xPos, yPos, imageWidth, imageHeight, PATH_IMAGE + "gt_dialog_background.jpg")
        self.addControl(self.imgBackground)

        self.lblTitle = xbmcgui.ControlLabel(xPos + 10, yPos + 5, imageWidth - 10, 20, "", "font14", "0xFF000000")  
        self.addControl(self.lblTitle)
        self.textBoxBody = xbmcgui.ControlTextBox(xPos + 10, yPos + 50, imageWidth - 20, imageHeight - 40, "font12", "0xFF000000")
        self.addControl(self.textBoxBody)
        
    def setTitle(self, title):
        self.lblTitle.setLabel(title)
        
    def setBody(self, body):
        self.textBoxBody.reset()
        self.textBoxBody.setText(body)
        print body

    def onAction(self, action):
        if action == ACTION_SELECT_ITEM:
            self.close()
        if (action == ACTION_PREVIOUS_MENU):
            self.close()
