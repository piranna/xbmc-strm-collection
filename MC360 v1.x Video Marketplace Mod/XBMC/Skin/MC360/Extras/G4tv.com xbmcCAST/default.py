#G4.py Version 0.1
#Author Greg Chrystall greg@chrystall.co.nz
#Script modded by Brad Quesnell 8bitbrad@gmail.com
#Note this is the first release, heavily copied from other XBMC Scripts.

import xml.dom.minidom, urllib, os, os.path, xbmc, xbmcgui, string, traceback, time

Emulating = "Emulating" in dir(xbmcgui)

ACTION_MOVE_LEFT        = 1     
ACTION_MOVE_RIGHT       = 2
ACTION_MOVE_UP          = 3
ACTION_MOVE_DOWN        = 4
ACTION_PAGE_UP          = 5
ACTION_PAGE_DOWN        = 6
ACTION_SELECT_ITEM      = 7
ACTION_HIGHLIGHT_ITEM   = 8
ACTION_PARENT_DIR       = 9
ACTION_PREVIOUS_MENU    = 10
ACTION_SHOW_INFO        = 11
ACTION_PAUSE            = 12
ACTION_STOP             = 13
ACTION_NEXT_ITEM        = 14
ACTION_PREV_ITEM        = 15

COORD_1080I      = 0 
COORD_720P       = 1 
COORD_480P_4X3   = 2 
COORD_480P_16X9  = 3 
COORD_NTSC_4X3   = 4 
COORD_NTSC_16X9  = 5 
COORD_PAL_4X3    = 6 
COORD_PAL_16X9   = 7 
COORD_PAL60_4X3  = 8 
COORD_PAL60_16X9 = 9

# dialog object for the whole app
dialog = xbmcgui.DialogProgress()

# Setup logging routines
ROOT_DIR = os.getcwd()[:-1]+'\\'
IMAGE_DIR = ROOT_DIR+'images\\'
DO_LOGGING = True
LOG_FILE_NAME = ROOT_DIR + "G4Log.txt"

if DO_LOGGING:
        LOG_FILE = open(LOG_FILE_NAME, 'w')

def LOG(message):
        if DO_LOGGING:
                LOG_FILE.write(str(message)+"\n")
                LOG_FILE.flush()

def LOGCLOSE():
        if DO_LOGGING:
                LOG_FILE.close()

itemElements            = ['title','link','pubDate', 'description']
rssFeeds                = {'Around the Net' : 'http://www.g4tv.com/dailynut/podcasts/15/The_Daily_Nut.xml',
                           'Attack of the Show' : 'http://www.g4tv.com/attackoftheshow/podcasts/5/Attack_of_the_Show_Daily_Video_Podcast.xml',
                           'AOTS: Fresh Ink' : 'http://www.g4tv.com/attackoftheshow/podcasts/21/AOTS_Fresh_Ink.xml',
                           'AOTS: In Your Pants' : 'http://www.g4tv.com/attackoftheshow/podcasts/22/AOTS_In_Your_Pants.xml',
                           'AOTS: Hardware' : 'http://www.g4tv.com/attackoftheshow/podcasts/23/AOTS_Hardware.xml',
                           'AOTS: Game Break' : 'http://www.g4tv.com/attackoftheshow/podcasts/24/AOTS_Game_Break.xml',
                           'The Block Podcast' : 'http://www.g4tv.com/theblock/podcasts/20/The_Block_Podcast.xml',
                           'G4tv.com Originals' : 'http://www.g4tv.com/g4originals/podcasts/25/G4tvcom_Originals.xml',
                           'Cheat!':'http://www.g4tv.com/cheat/podcasts/7/Cheat_Video_Podcast.xml',
                           'Cinematech':'http://www.g4tv.com/cinematech/podcasts/8/Cinematech_Video_Podcast.xml',
                           'Cinematech : Nocturnal Emissions':'http://www.g4tv.com/cinematechnocturnalemissions/podcasts/9/Cinematech_Nocturnal_Emissions_Video_Podcast.xml',
                           'Filter':'http://www.g4tv.com/filter/podcasts/10/Filter_Video_Podcast.xml',
                           'Formula D':'http://www.g4tv.com/formulad/podcasts/18/Formula_D_Video_Podcast.xml',
                           'Happy Tree Friends':'http://podcast.happytreefriends.com/htfrss.xml',
                           'Icons':'http://www.g4tv.com/icons/podcasts/17/ICONS_Video_Podcast.xml',
                           'Street Fury':'http://www.g4tv.com/streetfury/podcasts/11/Street_Fury_Video_Podcast.xml',
                           'The Feed':'http://www.g4tv.com/thefeed/podcasts/19/The_Daily_Feed_Video_Podcast.xml',
                           'The Man Show':'http://www.g4tv.com/themanshow/podcasts/14/The_Man_Show_Video_Podcast.xml',
                           'X-Play':'http://www.g4tv.com/xplay/podcasts/6/XPlay_Daily_Video_Podcast.xml'
                           }
                           
class G4Viewer(xbmcgui.Window):
        def __init__(self):
                self.setCoordinateResolution(COORD_NTSC_4X3)
                if Emulating: xbmcgui.Window.__init__(self)
                dialog.create("Getting RSS Feeds")
                self.feeds = {}
                self.urlsInOrder = []
                W = self.getWidth()
                H = self.getHeight()
                LOG("Image: " + IMAGE_DIR + 'background.png')
        	# background animation
                self.imgBackgroundani = xbmcgui.ControlImage(0, 0, 720, 476, "Q:\\Skin\\MC360\\Extras\\default-ani.gif")
                self.addControl(self.imgBackgroundani)
            
        	# background image
		self.imgBackgroundBlue = xbmcgui.ControlImage(0, 0, 720, 576, 'background-blue-alpha.png')
                self.addControl(self.imgBackgroundBlue)
                # custom background image
                self.imgCustomBackground = xbmcgui.ControlImage(0, 0, 720, 576, xbmc.getInfoLabel('Skin.String(Media)'))
                self.addControl(self.imgCustomBackground)
                self.imgCustomBackground.setColorDiffuse('D1FFFFFF')

        	# Whitewash glass top left
        	self.imgWhiteTL = xbmcgui.ControlImage(70, 0, 16, 64, 'bkgd-whitewash-glass-top-left.png')
        	self.addControl(self.imgWhiteTL)

        	# Whitewash glass top middle
        	self.imgWhiteTMID = xbmcgui.ControlImage(86, 0, 592, 64, 'bkgd-whitewash-glass-top-middle.png')
        	self.addControl(self.imgWhiteTMID)

        	# Whitewash glass top right
        	self.imgWhiteTR = xbmcgui.ControlImage(678, 0, 16, 64, 'bkgd-whitewash-glass-top-right.png')
        	self.addControl(self.imgWhiteTR)

        	# Whitewash glass bottom left
        	self.imgWhiteBL = xbmcgui.ControlImage(70, 412, 16, 64, 'bkgd-whitewash-glass-bottom-left.png')
        	self.addControl(self.imgWhiteBL)

        	# Whitewash glass bottom middle
        	self.imgWhiteBMID = xbmcgui.ControlImage(86, 412, 592, 64, 'bkgd-whitewash-glass-bottom-middle.png')
        	self.addControl(self.imgWhiteBMID)

        	# Whitewash glass bottom right
        	self.imgWhiteBR = xbmcgui.ControlImage(678, 412, 16, 64, 'bkgd-whitewash-glass-bottom-right.png')
        	self.addControl(self.imgWhiteBR)

        	# Whitewash overlay left
        	self.imgWhitewashL = xbmcgui.ControlImage(60, 0, 32, 476, 'background-overlay-whitewash-left.png')
        	self.addControl(self.imgWhitewashL)

        	# Whitewash overlay middle
        	self.imgWhitewashMID = xbmcgui.ControlImage(92, 0, 553, 476, 'background-overlay-whitewash-centertile.png')
        	self.addControl(self.imgWhitewashMID)

        	# Whitewash overlay right
        	self.imgWhitewashR = xbmcgui.ControlImage(645, 0, 64, 476, 'background-overlay-whitewash-right.png')
        	self.addControl(self.imgWhitewashR)

        	# Left blade runner
        	self.imgBladerunL = xbmcgui.ControlImage(-61, 0, 128, 476, 'blades-runner-left.png')
        	self.addControl(self.imgBladerunL)

        	# Right blade runner
        	self.imgBladerunR = xbmcgui.ControlImage(665, 0, 128, 476, 'blades-runner-right.png')
        	self.addControl(self.imgBladerunR)

        	# Header Blade
        	self.imgBlade = xbmcgui.ControlImage(18, 0, 80, 476, 'blades-size4-header.png')
        	self.addControl(self.imgBlade)

        	# Y Button
        	self.imgybutton = xbmcgui.ControlImage(125, 420, 21, 21, 'button-Y-turnedoff.png')
        	self.addControl(self.imgybutton)

        	# X Button
        	self.imgxbutton = xbmcgui.ControlImage(112, 440, 21, 21, 'button-X.png')
        	self.addControl(self.imgxbutton)

        	# Back Button
        	self.imgbackbutton = xbmcgui.ControlImage(620, 420, 21, 21, 'button-back.png')
        	self.addControl(self.imgbackbutton)

        	# A Button
        	self.imgabutton = xbmcgui.ControlImage(633, 440, 21, 21, 'button-A.png')
        	self.addControl(self.imgabutton)

                self.medialabel           = xbmcgui.ControlLabel(79,129,100,20,'media','font14','0xFF000000',angle=270)
                self.g4label           = xbmcgui.ControlLabel(95,30,375,20,'G4tv.com xbmcCast','font18','0xFFFFFFFF')
                self.vislabel           = xbmcgui.ControlLabel(145,443,375,20,'Full Screen Visualization','font12','0xFFFFFFFF')
                self.backlabel           = xbmcgui.ControlLabel(580,423,80,20,'Back','font12','0xFFFFFFFF')
                self.selectlabel           = xbmcgui.ControlLabel(577,443,80,20,'Select','font12','0xFFFFFFFF')
                
                
                self.shows              = xbmcgui.ControlList(87,64,140,390,'font13','0xFF000000')
                self.itemList           = xbmcgui.ControlList(290,64,375,390,'font13','0xFF000000')
                self.addControl(self.medialabel)
                self.addControl(self.g4label) 
                self.addControl(self.vislabel)
                self.addControl(self.backlabel)
                self.addControl(self.selectlabel)               
                self.addControl(self.shows)
                self.addControl(self.itemList)
                #Move left and right.
                self.shows.controlRight(self.itemList)
                self.shows.controlLeft(self.itemList)
                self.itemList.controlRight(self.shows)
                self.itemList.controlLeft(self.shows)
                count = 1.0
                for name, url in sorted(rssFeeds.iteritems()):
                        progress = int(((count / float(len(rssFeeds))) * 100.0))
                        dialog.update(progress, "Getting " + name + " RSS Feed.")
                        #self.feeds[name] = FeedItems(url).getData()
                        self.shows.addItem(name)
                        count = count + 1.0
                dialog.close()
                #self.updateItems('G4')
                self.setFocus(self.shows)
                
        def onAction(self, action):
                if action == ACTION_PREVIOUS_MENU:
                        if DO_LOGGING:
                                LOGCLOSE()
                        self.close()
        
        def onControl(self, control):
                if(control == self.itemList):
                        try:
                                LOG("Item list clicked...")
                                LOG(self.itemList.getSelectedPosition())
                                position = self.itemList.getSelectedPosition()
                                filename = self.urlsInOrder[position]
                                LOG("Playing: " + filename)
                                if filename:
                                        LOG("Before Player Call")
                                        try:
                                                xbmc.Player().play(str(filename))
                                        except:
                                                LOG("Player Exception")
                                        LOG("After Player Call")
                                else:
                                        xbmcgui.Dialog().ok('ERROR', 'Most likely video unavailable for download.')
                        except:
                                xbmc.output('ERROR: playing %s' % ( filename) )
                        
                if(control == self.shows):
                        print "Clicked: "
                        self.changeShow(self.shows.getSelectedItem().getLabel())
        
        def changeShow(self, show):
                dialog.create("Getting " + show + " RSS Feed.")
                self.updateItems(show)
                dialog.close()
        
        def updateItems(self, show):
                LOG("rssFeeds Keys:")
                for key in rssFeeds.keys():
                        LOG(key)
                if(rssFeeds.has_key("G4")):
                        LOG("HAS G4!")
                        LOG(str(rssFeeds["G4"]))
                if(not self.feeds.has_key(show)):
                        try:
                                self.feeds[show] = FeedItems(rssFeeds[show]).getData()
                        except:
                                xbmcgui.Dialog().ok("Error", "Could not get rss feed: '" + show + "'")
                                return
                self.itemList.reset()
                self.urlsInOrder = None
                self.urlsInOrder = []
                for item in self.feeds[show]:
                        self.itemList.addItem(item.getElement("title"))
                        self.urlsInOrder.append(item.getElement("mediaUrl"))
        
        def cancelOpen():
                if DO_LOGGING:
                        LOGCLOSE()
                self.close()



class FeedItems:
        def __init__(self, url):
                self.dom = None
                f = urllib.urlopen(url)
                xmlDocument = f.read()
                f.close()
                self.dom = xml.dom.minidom.parseString(xmlDocument)
                self.data = []
                self.extractURLNameDictionary()
                
        
        def extractURLNameDictionary(self):
                items = self.dom.getElementsByTagName("item")
                for item in items:
                        elements = {}
                        for itemElement in itemElements:
                                try:
                                        elements[itemElement] = item.getElementsByTagName(itemElement)[0].childNodes[0].data.strip()
                                        #print itemElement, " = ", item.getElementsByTagName(itemElement)[0].childNodes[0].data
                                except:
                                        pass
                        try:
                                elements["mediaUrl"] = item.getElementsByTagName("enclosure")[0].getAttribute("url").strip()
                        except:
                                try:
                                        elements["mediaUrl"] = item.getElementsByTagName("link")[0].childNodes[0].data.strip()
                                except: 
                                        xbmcgui.Dialog().ok("Error", "Problem building feed.")
                        self.data.append(RSSItem(elements))
                
        def getData(self):
                return self.data
class RSSItem:
        def __init__(self, elements):
                # list that includes required item elements
                self.elements = elements
                
        def getElement(self, element):
                return self.elements[element]
                
        def getElementNames(self):
                return self.elements.keys()
                
        def hasElement(self, element):
                return self.elements.has_key(element)
        
w = G4Viewer()
w.doModal()
del w


