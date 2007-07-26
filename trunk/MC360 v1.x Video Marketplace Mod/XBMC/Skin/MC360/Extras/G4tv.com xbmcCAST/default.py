#G4.py Version 0.3
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
                           'G4tv.com Originals' : 'http://www.g4tv.com/g4originals/podcasts/25/G4tvcom_Originals.xml',
                           'Cheat!':'http://www.g4tv.com/cheat/podcasts/7/Cheat_Video_Podcast.xml',
                           'Cinematech':'http://www.g4tv.com/cinematech/podcasts/8/Cinematech_Video_Podcast.xml',
                           'Cinematech : Nocturnal Emissions':'http://www.g4tv.com/cinematechnocturnalemissions/podcasts/9/Cinematech_Nocturnal_Emissions_Video_Podcast.xml',
                           'Happy Tree Friends':'http://podcast.happytreefriends.com/htfrss.xml',
                           'ICONS':'http://www.g4tv.com/icons/podcasts/17/ICONS_Video_Podcast.xml',
                           'Street Fury':'http://www.g4tv.com/streetfury/podcasts/11/Street_Fury_Video_Podcast.xml',
                           'The Daily Feed':'http://www.g4tv.com/thefeed/podcasts/19/The_Daily_Feed_Video_Podcast.xml',
                           'The Man Show':'http://www.g4tv.com/themanshow/podcasts/14/The_Man_Show_Video_Podcast.xml',
                           'X-Play':'http://www.g4tv.com/xplay/podcasts/6/XPlay_Daily_Video_Podcast.xml',
                           'Ninja Warrior':'http://www.g4tv.com/ninjawarrior/podcasts/27/Ninja_Warrior_Video_Podcast.xml',
                           'Freestyle 101':'http://www.g4tv.com/g4originals/podcasts/26/Freestyle_101_Video_Podcast.xml'
                           }
                           
class G4Viewer(xbmcgui.Window):
        def __init__(self):
                if Emulating: xbmcgui.Window.__init__(self)
                dialog.create("Getting RSS Feeds")
                self.feeds = {}
                self.urlsInOrder = []
                
                #xbmcgui.lock()

		if xbmc.getSkinDir() == 'MC360':
			# Get scaling info
			self.scaleX = ( float(self.getWidth())  / float(720) )
			self.scaleY = ( float(self.getHeight()) / float(480) )

			# Create static controls
			self.addControl(xbmcgui.ControlImage(0,0, int(720*self.scaleX),int(480*self.scaleY), 'background-blue.png'))
			self.addControl(xbmcgui.ControlImage(18,0, int(720*self.scaleX),int(480*self.scaleY), xbmc.getInfoLabel('Skin.String(Media)')))
			self.addControl(xbmcgui.ControlImage(int(70*self.scaleX),0, int(16*self.scaleX),int(54*self.scaleY), 'bkgd-whitewash-glass-top-left.png'))
			self.addControl(xbmcgui.ControlImage(int(86*self.scaleX),0, int(667*self.scaleX),int(54*self.scaleY), 'bkgd-whitewash-glass-top-middle.png'))
			self.addControl(xbmcgui.ControlImage(int(753*self.scaleX),0, int(16*self.scaleX),int(54*self.scaleY), 'bkgd-whitewash-glass-top-right.png'))
			self.addControl(xbmcgui.ControlImage(int(86*self.scaleX),int(427*self.scaleY), int(667*self.scaleX),int(54*self.scaleY), 'bkgd-whitewash-glass-bottom-middle.png'))
			self.addControl(xbmcgui.ControlImage(int(70*self.scaleX),int(427*self.scaleY), int(16*self.scaleX),int(54*self.scaleY), 'bkgd-whitewash-glass-bottom-left.png'))
			self.addControl(xbmcgui.ControlImage(int(753*self.scaleX),int(427*self.scaleY), int(667*self.scaleX),int(54*self.scaleY), 'bkgd-whitewash-glass-bottom-right.png'))
			self.addControl(xbmcgui.ControlImage(int(60*self.scaleX),0, int(32*self.scaleX),int(480*self.scaleY), 'background-overlay-whitewash-left.png'))
			self.addControl(xbmcgui.ControlImage(int(92*self.scaleX),0, int(628*self.scaleX),int(480*self.scaleY), 'background-overlay-whitewash-centertile.png'))
			self.addControl(xbmcgui.ControlImage(int(-61*self.scaleX),0, int(128*self.scaleX),int(480*self.scaleY), 'blades-runner-left.png'))
			self.addControl(xbmcgui.ControlImage(int(18*self.scaleX),0, int(80*self.scaleX),int(480*self.scaleY), 'blades-size4-header.png'))
			self.addControl(xbmcgui.ControlLabel(int(155*self.scaleX),int(35*self.scaleY), int(200*self.scaleX),int(35*self.scaleY), 'xbmcCAST', font="font18"))
			self.addControl(xbmcgui.ControlLabel(int(79*self.scaleX),int(129.1666*self.scaleY), int(270*self.scaleX),int(35*self.scaleY), 'media',angle=270,textColor="0xFF000000",font="font14"))
			

			# Create button images and descriptions
			
			#self.y_img = xbmcgui.ControlImage(int(125*self.scaleX),int(420*self.scaleY), int(21*self.scaleX),int(18*self.scaleY), 'button-Y.png')
			#self.addControl(self.y_img)
			#self.y_desc = xbmcgui.ControlLabel(int(155*self.scaleX),int(420*self.scaleY), int(200*self.scaleX),int(35*self.scaleY), 'Action 2',font="font12")
			#self.addControl(self.y_desc)
			#self.y_on = 1

			self.x_img = xbmcgui.ControlImage(int(110*self.scaleX),int(440*self.scaleY), int(21*self.scaleX),int(18*self.scaleY), 'button-Back.png')
			self.addControl(self.x_img)
			self.x_desc = xbmcgui.ControlLabel(int(140*self.scaleX),int(440*self.scaleY), int(200*self.scaleX),int(35*self.scaleY), 'Exit',font="font12")
			self.addControl(self.x_desc)
			self.x_on = 1

			#self.b_img = xbmcgui.ControlImage(int(610*self.scaleX),int(420*self.scaleY), int(21*self.scaleX),int(18*self.scaleY), 'button-B-turnedoff.png')
			#self.addControl(self.b_img)
			#self.b_desc = xbmcgui.ControlLabel(int(600*self.scaleX),int(420*self.scaleY), int(200*self.scaleX),int(35*self.scaleY), 'Back',alignment=1,font="font12")
			#self.addControl(self.b_desc)
			#self.x_on = 0



			self.a_img = xbmcgui.ControlImage(int(625*self.scaleX),int(440*self.scaleY), int(21*self.scaleX),int(18*self.scaleY), 'button-A.png')
			self.addControl(self.a_img)
			self.a_desc = xbmcgui.ControlLabel(int(615*self.scaleX),int(440*self.scaleY), int(200*self.scaleX),int(35*self.scaleY), 'Select',alignment=1,font="font12")
			self.addControl(self.a_desc)

			self.addControl(xbmcgui.ControlImage(90, 3, 60, 60,ROOT_DIR + 'default.tbn'))

			# Create list
			self.list = xbmcgui.ControlList(int(90*self.scaleX), int(70*self.scaleY), int(610*self.scaleX), int(340*self.scaleY),"font13","0xFF000000","iconlist-nofocus.png","iconlist-focus.png",itemTextXOffset=4,imageWidth=32, imageHeight=32,itemHeight=40)
			self.addControl(self.list)
		else:
			# Get scaling info
			self.scaleX = ( float(self.getWidth())  / float(720) )
			self.scaleY = ( float(self.getHeight()) / float(576) )

			#LIST

                self.shows              = xbmcgui.ControlList(100,66,160,370,'font13','0xFF000000',itemTextXOffset=-10)
                self.itemList           = xbmcgui.ControlList(270,66,420,370,'font13','0xFF000000')
                
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


