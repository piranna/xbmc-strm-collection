'''
This file is part of the 'XBMC GameTrailersRssReader script'.

'XBMC GameTrailersRssReader script' is free software; you can redistribute it
and/or modify it under the terms of the GNU General Public License as 
published by the Free Software Foundation; either version 2 of the License,
or (at your option) any later version.

'XBMC GameTrailersRssReader script' is distributed in the hope that it will 
be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with software; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''
import xbmc, xbmcgui
import xml.dom.minidom, sys, urllib, os, string

try: Emulating = xbmcgui.Emulating
except: Emulating = False

if (not Emulating): sys.path.append(sys.path[0] + '\\lib')
import cachedhttp, textwindow, rss

try:
   reload(gtweb)
except:
   import gtweb
try:
   reload(gt)
except:
   import gt


#
# Path init
#

PATH_ROOT = os.getcwd().replace(";","") + "\\"
if Emulating: PATH_IMAGE = PATH_ROOT + "../img/"
else: PATH_IMAGE = PATH_ROOT + "img\\"
PATH_DOWNLOAD = PATH_ROOT + "download\\"


# RSS elements that is read by the RSSParser class when parsing the RSS
RSS_CHANNEL_ELEMENTS    = ['title','link','description']
RSS_ITEM_ELEMENTS        = ['exInfo:gameID', 'exInfo:gameName','exInfo:movieTitle','description','pubDate', 'exInfo:image','exInfo:downloadsThisWeek', 'exInfo:totalDownloads', 'rating', 'guid']

COORD_1080I      = 0 # HDTV_1080i = 0,   (1920x1080, 16:9, pixels are 1:1)
COORD_720P       = 1 # HDTV_720p = 1,   (1280x720, 16:9, pixels are 1:1)
COORD_480P_4X3   = 2 # HDTV_480p_4x3 = 2,   (720x480, 4:3, pixels are 4320:4739)
COORD_480P_16X9  = 3 # HDTV_480p_16x9 = 3,   (720x480, 16:9, pixels are 5760:4739)
COORD_NTSC_4X3   = 4 # NTSC_4x3 = 4,   (720x480, 4:3, pixels are 4320:4739)
COORD_NTSC_16X9  = 5 # NTSC_16x9 = 5,   (720x480, 16:9, pixels are 5760:4739)
COORD_PAL_4X3    = 6 # PAL_4x3 = 6,       (720x576, 4:3, pixels are 128:117)
COORD_PAL_16X9   = 7 # PAL_16x9 = 7,     (720x576, 16:9, pixels are 512:351)
COORD_PAL60_4X3  = 8 # PAL60_4x3 = 8,   (720x480, 4:3, pixels are 4320:4739)
COORD_PAL60_16X9 = 9 # PAL60_16x9 = 9   (720x480, 16:9, pixels are 5760:4739)

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
ACTION_MUSIC_PLAY       = 79
ACTION_CONTEXT_MENU     = 117


DISPLAY_TRAILERS = 0
DISPLAY_SEARCH_RESULT = 1
DISPLAY_GAME = 2

DOWNLOAD_TYPE_TRAILER_PAGE = 0
DOWNLOAD_TYPE_RSS = 1


MENU_X_POS = 95
MENU_Y_POS = 80
MENU_HEIGHT = 25
MENU_WIDTH = 170
MENU_SUB_Y_POS = 230
MENU_SUB_HEIGHT = 24

INFO_Y_POS = 55
INFO_HEIGHT = 25
INFO_KEY_X_POS = 310
INFO_KEY_WIDTH = 100
INFO_VALUE_X_POS = 420
INFO_VALUE_WIDTH = 300

VERSION_STR = "0.4.2"

class MyClass(xbmcgui.Window):

    def __init__(self):
        if Emulating: xbmcgui.Window.__init__(self)
        self.setCoordinateResolution(COORD_PAL_4X3) # scales objects automatically

        # background animation
        self.imgBackgroundani = xbmcgui.ControlImage(0, 0, 720, 576, "Q:\\skin\\MC360\\Extras\\background-ani.gif")
        self.addControl(self.imgBackgroundani)

        # background image
        self.imgBackground = xbmcgui.ControlImage(0, 0, 720, 576, 'background-blue-alpha.png')
        self.addControl(self.imgBackground)

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
        self.imgWhiteBL = xbmcgui.ControlImage(70, 512, 16, 64, 'bkgd-whitewash-glass-bottom-left.png')
        self.addControl(self.imgWhiteBL)

        # Whitewash glass bottom middle
        self.imgWhiteBMID = xbmcgui.ControlImage(86, 512, 592, 64, 'bkgd-whitewash-glass-bottom-middle.png')
        self.addControl(self.imgWhiteBMID)

        # Whitewash glass bottom right
        self.imgWhiteBR = xbmcgui.ControlImage(678, 512, 16, 64, 'bkgd-whitewash-glass-bottom-right.png')
        self.addControl(self.imgWhiteBR)

        # Whitewash overlay left
        self.imgWhitewashL = xbmcgui.ControlImage(60, 0, 32, 576, 'background-overlay-whitewash-left.png')
        self.addControl(self.imgWhitewashL)

        # Whitewash overlay middle
        self.imgWhitewashMID = xbmcgui.ControlImage(92, 0, 553, 576, 'background-overlay-whitewash-centertile.png')
        self.addControl(self.imgWhitewashMID)

        # Whitewash overlay right
        self.imgWhitewashR = xbmcgui.ControlImage(645, 0, 64, 576, 'background-overlay-whitewash-right.png')
        self.addControl(self.imgWhitewashR)

        # Left blade runner
        self.imgBladerunL = xbmcgui.ControlImage(-61, 0, 128, 576, 'blades-runner-left.png')
        self.addControl(self.imgBladerunL)

        # Right blade runner
        self.imgBladerunR = xbmcgui.ControlImage(665, 0, 128, 576, 'blades-runner-right.png')
        self.addControl(self.imgBladerunR)

        # Header Blade
        self.imgBlade = xbmcgui.ControlImage(18, 0, 80, 576, 'blades-size4-header.png')
        self.addControl(self.imgBlade)

        # Y Button
        self.addControl(xbmcgui.ControlImage(125, 520, 21, 21, 'button-Y-turnedoff.png'))
        # X Button
        self.addControl(xbmcgui.ControlImage(112, 540, 21, 21, 'button-X.png'))
        # Back Button
        self.addControl(xbmcgui.ControlImage(620, 520, 21, 21, 'button-back.png'))
        # A Button
        self.addControl(xbmcgui.ControlImage(633, 540, 21, 21, 'button-A.png'))
        self.addControl(xbmcgui.ControlLabel(79,149,100,20,'media','font14','0xFF000000',angle=270))
        self.addControl(xbmcgui.ControlLabel(145,543,375,20,'Full Screen Visualization','font12','0xFFFFFFFF'))
        self.addControl(xbmcgui.ControlLabel(580,523,80,20,'Back','font12','0xFFFFFFFF'))
        self.addControl(xbmcgui.ControlLabel(577,543,80,20,'Select','font12','0xFFFFFFFF'))

 
        # top title bar with channel info
        if (Emulating): self.lblScreenTitle = xbmcgui.ControlLabel(102, 42, 620, 10, "font18", "0xFFFFFFFF")
        else: self.lblScreenTitle = xbmcgui.ControlFadeLabel(102, 42, 620, 10, "font18", "0xFFFFFFFF")
        self.addControl(self.lblScreenTitle)
        self.setTitle("GameTrailers.com - RSS Reader v" + VERSION_STR)

        # bottom bar with copyright stuff
        self.lblCopyright = xbmcgui.ControlFadeLabel(70, 570, 550, 10, "font12", "0xFFFFFFFF")
        self.addControl(self.lblCopyright)
        self.lblCopyright.addLabel("All logotypes, videos, text is Copyright (c) 2005 Gametrailers.com, all rights reserved.")
        self.lblCopyright.addLabel("GameTrailers.com RSS Reader v" + VERSION_STR + " developed by RedSolo. For latest version check www.xbmcscripts.com.")
        
        self.isGameInfoVisible = True
        self.lblInfoKeys = []
        self.lblInfoValues = []
        self.lblInfoNextYPos = INFO_Y_POS        
        self.addInfoLabel("Release")
        self.addInfoLabel("Platforms")
        self.addInfoLabel("Publisher")
        self.addInfoLabel("Developer")
        self.addInfoLabel("Genres")
        self.addInfoLabel("ESRB")
        self.imgBoxArt = None

        # media list
        if (Emulating): self.listMedia = xbmcgui.ControlList(290, 85 + 162, 375, 390 - 200, "font14", "0xFF000000")
        else: self.listMedia = xbmcgui.ControlList(290, 85, 375, 390, "font14", "0xFF000000")
        self.listMedia.setItemHeight(30)
        self.addControl(self.listMedia)

        self.btnNextYPos = MENU_Y_POS
        self.btnTemp = None

        self.mapMenu = {}
        self.btnMenuFirst = None
        self.btnMenuLast = None
        self.btnMenuNewest = self.addMenu("Newest", "newest", DOWNLOAD_TYPE_RSS)
        self.btnMenuTop20 = self.addMenu("Top Media", "top20", DOWNLOAD_TYPE_TRAILER_PAGE)
        self.btnMenuTopRated = self.addMenu("Top Rated", "toprated", DOWNLOAD_TYPE_TRAILER_PAGE)
        self.btnMenuTopRated = self.addMenu("Reviews", "reviews", DOWNLOAD_TYPE_TRAILER_PAGE)
        self.btnMenuTopRated = self.addMenu("GT.Tv", "topgttv", DOWNLOAD_TYPE_TRAILER_PAGE)
        self.btnMenuSearch = self.addMenu("Search", "search", None)
        self.btnMenuLast.controlDown(self.btnMenuFirst)
        self.btnMenuFirst.controlUp(self.btnMenuLast)
        self.ctrlCurrentMainMenu = None
        
        self.isSubMenuVisible = True
        self.mapSubMenu = {}
        self.btnNextYPos = MENU_SUB_Y_POS
        self.btnSubMenuFirst = None
        self.btnSubMenuLast = None
        self.btnSubMenuAll = self.addSubMenu("All", "")
        self.btnSubMenuPC = self.addSubMenu("PC", "pc")
        self.btnSubMenuPs2 = self.addSubMenu("Playstation 2", "ps2")
        self.btnSubMenuPs3 = self.addSubMenu("Playstation 3", "ps3")
        self.btnSubMenuXbox = self.addSubMenu("Xbox", "xbox")
        self.btnSubMenuXbox360 = self.addSubMenu("Xbox 360", "xb360")
        self.btnSubMenuGc = self.addSubMenu("Gamecube", "gc")
        self.btnSubMenuWii = self.addSubMenu("Nintendo Wii", "rev")
        self.btnSubMenuDS = self.addSubMenu("Nintendo DS", "ds")
        self.btnSubMenuGba = self.addSubMenu("GameBoy Adv", "gba")
        self.btnSubMenuPsp = self.addSubMenu("PSP", "psp")
        #self.btnSubMenuNgage = self.addSubMenu("N-Gage", "ngage")
        #self.btnSubMenuHand = self.addSubMenu("Handhelds", "hand")

        self.imgSubMenuTop = xbmcgui.ControlImage(MENU_X_POS, MENU_SUB_Y_POS - MENU_SUB_HEIGHT, MENU_WIDTH, MENU_SUB_HEIGHT, PATH_IMAGE + "fuckthisimage.jpg")
        self.addControl(self.imgSubMenuTop)
        self.imgSubMenuBottom = xbmcgui.ControlImage(MENU_X_POS, self.btnNextYPos, MENU_WIDTH, MENU_SUB_HEIGHT, PATH_IMAGE + "fuckthisimage.jpg")
        self.addControl(self.imgSubMenuBottom)
        
        self.listMedia.controlLeft(self.btnMenuNewest)
        self.setFocus(self.btnMenuNewest)
        
        self.setSubMenuVisible(False)
        self.setGameInfoVisible(False)

        # Web objects
        self.httpFetcher=cachedhttp.CachedHTTPWithProgress()
        self.gtWeb = gtweb.GtPage(self.httpFetcher)
        self.rssParser = rss.RSSParser(RSS_CHANNEL_ELEMENTS , RSS_ITEM_ELEMENTS)

        self.mediaTrailers = None
        self.searchResult = None

        self.displayState = DISPLAY_TRAILERS
        self.searchStr = ""
            
    def onAction(self, action):
        if (action == ACTION_PREVIOUS_MENU):
            self.close()
        if (action == ACTION_CONTEXT_MENU):
            if (self.getFocus() == self.listMedia) and (self.displayState == DISPLAY_TRAILERS):
                self.onContextMenuClick()
        if (action == ACTION_MUSIC_PLAY):
            if (self.getFocus() == self.listMedia) and (self.displayState == DISPLAY_TRAILERS):
                self.onListControlClick()
        if (action == ACTION_SHOW_INFO):
            if (self.getFocus() == self.listMedia) and (self.displayState == DISPLAY_TRAILERS):
                self.onDisplayGame()
        if Emulating:
            if (action == ACTION_SELECT_ITEM):
                self.onListControlClick()
            if (action == ACTION_MOVE_UP):
                self.onDisplayGame()
            if (action == ACTION_MOVE_DOWN):                
                self.downloadAndPlay()
            if (action == ACTION_MOVE_RIGHT):                
                self.onContextMenuClick()
            
    def onControl(self, control):        
        if (control == self.listMedia):
            self.onListControlClick()
        if (self.mapMenu.has_key(control.getId())):
            self.onMainMenuClick(control)
        if (self.mapSubMenu.has_key(control.getId())):
            self.onSubMenuClick(control)

    def onContextMenuClick(self):
        choices = ["Show game info", "Play trailer", "Download & play"]
        if (self.searchResult <> None):
            choices.append("Last search result")
        dialog = xbmcgui.Dialog()
        choice = dialog.select("Game menu", choices)
        if choice == 0: self.onDisplayGame()
        if choice == 1: self.playMedia()
        if choice == 2: self.downloadAndPlay()
        if choice == 3: self.displayTrailerList(searchResult)
        
    def onMainMenuClick(self, control):
        self.listMedia.controlLeft(control)
        self.ctrlCurrentMainMenu = self.mapMenu[control.getId()]
        if (control == self.btnMenuSearch):
            self.setSubMenuVisible(False)
            self.searchForGame()
        else:
            self.setSubMenuVisible(True)
            if (self.ctrlCurrentMainMenu.downloadType == DOWNLOAD_TYPE_RSS):
                self.downloadRss(self.ctrlCurrentMainMenu.getLinkStr())
            else:
                self.setTitle("GameTrailers.com - " + self.ctrlCurrentMainMenu.getFullName())
                self.displayTrailerList(self.gtWeb.retrieveTrailers(self.ctrlCurrentMainMenu.getLinkStr(), None))   

    def onSubMenuClick(self, control):
        self.listMedia.controlLeft(control)
        subMenu = self.mapSubMenu[control.getId()]
        if (self.ctrlCurrentMainMenu.downloadType == DOWNLOAD_TYPE_RSS):
            if (control == self.btnSubMenuWii):
                self.showMessageBox("GameTrailers.com has no RSS for the Nintendo Wii. Sorry.")
            else:
                self.downloadRss(self.ctrlCurrentMainMenu.getLinkStr(), subMenu.getLinkStr())
        else:
            self.setTitle("GameTrailers.com - " + self.ctrlCurrentMainMenu.getFullName() + " - " + subMenu.getFullName())
            self.displayTrailerList(self.gtWeb.retrieveTrailers(self.ctrlCurrentMainMenu.getLinkStr(), subMenu.getLinkStr()))  

    def onListControlClick(self):
        if (self.displayState == DISPLAY_SEARCH_RESULT):
            if (len(self.searchResult) > 0):
                game = self.searchResult[self.listMedia.getSelectedPosition()]
                if (game <> None):
                    self.displayGame(game.guid)
        else:
            self.playMedia()

    def onDisplayGame(self):
        if (len(self.mediaTrailers) == 0):
            return        
        trailer = self.mediaTrailers[self.listMedia.getSelectedPosition()]
        if (trailer == None):
            return
        self.displayGame(trailer.gameGuid)

    def setTitle(self, text):
        if (Emulating):
            self.lblScreenTitle.setLabel(text)
        else:
            self.lblScreenTitle.reset()
            self.lblScreenTitle.addLabel(text)
    
    def showMessageBox(self, body, title = None ):
        dialog = textwindow.Dialog()
        if (title <> None):
            dialog.setTitle(title)
        dialog.setBody(body)
        dialog.doModal()
        
    def updateBoxArt(self, boxArtLink):
        if (self.imgBoxArt <> None):
            self.removeControl(self.imgBoxArt)        
        try:
            localFile = self.httpFetcher.urlretrieve(boxArtLink)
            self.imgBoxArt = xbmcgui.ControlImage(200, 60, 70 * 1.4, 100 * 1.4, localFile)
            self.addControl(self.imgBoxArt)
        except:
            self.imgBoxArt = None
            if (Emulating): raise

    def displayGameList(self, gameList):
        self.listMedia.reset()
        self.listMedia.setImageDimensions(60,74)
        xbmcgui.lock()
        self.mediaTrailers = None
        shouldDisplayBoxArt = len(gameList) < 20
        for game in gameList:
            listItem = xbmcgui.ListItem(game.toString())            
            if (shouldDisplayBoxArt and (game.boxArtLink <> None)):
                try:
                    imageUrl = game.boxArtLink
                    localFile = self.httpFetcher.urlretrieve(imageUrl)
                    listItem.setThumbnailImage(localFile)
                except:
                    pass
            self.listMedia.addItem(listItem)
        xbmcgui.unlock()

    def displayTrailerList(self, trailerList):
        self.listMedia.reset()
        self.listMedia.setImageDimensions(178,74)
        xbmcgui.lock()
        self.mediaTrailers = trailerList
        for trailer in self.mediaTrailers:
            listItem = xbmcgui.ListItem(trailer.toString())
            if (trailer.thumbnailLink <> None):
                try:
                    imageUrl = trailer.thumbnailLink
                    localFile = self.httpFetcher.urlretrieve(imageUrl)
                    listItem.setThumbnailImage(localFile)
                except:
                    pass
            self.listMedia.addItem(listItem)
        xbmcgui.unlock()
        
    def displayGame(self, guid):
        try:
            self.clearGame()
            self.listMedia.reset()
            game = self.gtWeb.retrieveGameInfo(guid)
            self.setDisplayState(DISPLAY_GAME)
            self.setTitle(game.name)
            self.lblInfoValues[0].setLabel(game.release)
            self.lblInfoValues[1].setLabel(game.getPlatformStr())
            self.lblInfoValues[2].setLabel(game.publisher)
            self.lblInfoValues[3].setLabel(game.developer)
            self.lblInfoValues[4].setLabel(game.genres)
            self.lblInfoValues[5].setLabel(game.rating)
            self.updateBoxArt(game.boxArtLink)
            self.displayTrailerList(self.gtWeb.retrieveGameTrailerList(guid))
        except:
            self.showMessageBox("There was a problem downloading the game information, either GameTrailers has changed the media links or the game is not currently available. Actual error: " + str(sys.exc_info()[0]), "Error")
            if (Emulating): raise
        
    def clearGame(self):
        self.setTitle("")
        self.lblInfoValues[0].setLabel("")
        self.lblInfoValues[1].setLabel("")
        self.lblInfoValues[2].setLabel("")
        self.lblInfoValues[3].setLabel("")
        self.lblInfoValues[4].setLabel("")
        self.lblInfoValues[5].setLabel("")
        if (self.imgBoxArt <> None):
            self.removeControl(self.imgBoxArt)
            self.imgBoxArt = None
        
    def searchForGame(self, searchStr = None, platformStr = None):
        if (searchStr == None):            
            if Emulating: dialog = xbmc.Keyboard()
            else: dialog = xbmc.Keyboard(self.searchStr, "Enter the search string")
            dialog.doModal()
            if (dialog.isConfirmed()):
                self.searchStr = dialog.getText()
                searchStr = self.searchStr

        if (searchStr <> None):
            try:
                title = "GameTrailers.com - Searching for '" + self.searchStr + "'"
                if (platformStr <> None):
                    title = title + " - " + platformStr
                self.setTitle(title)
                self.searchResult = self.gtWeb.gameSearch(self.searchStr, platformStr)                
                self.setDisplayState( DISPLAY_SEARCH_RESULT )
                title = "GameTrailers.com - Search result for '" + self.searchStr + "'"
                if (platformStr <> None):
                    title = title + " - " + platformStr
                self.setTitle(title)
                self.displayGameList(self.searchResult)
            except:
                self.showMessageBox("There was a problem searching for a game. GameTrailers has probably changed the search links. Actual error: " + str(sys.exc_info()[0]), "Error")
                if (Emulating): raise

    def downloadRss(self, feedName, platformName = None):
        '''
            downloadRss(string feedName, string platformName) -- .

            feedName     : name of the feed to download, ie newest, top20, toprated
            platformName : name of the specific platform to download, pc, ps2, ps3. If none, rss for all platforms will be downloaded.
        '''
        #xbmcgui.lock()
        try:
            url = "http://www.gametrailers.com/rss/"
            url = url + feedName
    
            if (platformName <> None):
                url = url + platformName
            url = url + ".xml"
            
            rssFeedFile = self.httpFetcher.urlretrieve(url)
            
            self.rssParser.feedFromFile(rssFeedFile)
            self.rssParser.parse()
                        
            text = self.rssParser.getChannelInfo().getElement("title")
            print text
            if (self.mapSubMenu.has_key(self.getFocus().getId())):
                text = text + " - " + self.mapSubMenu[self.getFocus().getId()].getFullName()
            else:
                text = text + " - All"        
            self.setTitle(text)

            self.setDisplayState( DISPLAY_TRAILERS )
            trailers = []
            for item in self.rssParser.getItems():            
                trailer = gt.Trailer()
                trailer.copyFromRssItem(item)
                trailers.append(trailer)
            self.displayTrailerList(trailers)
            
        except :            
            self.showMessageBox("There was a problem downloading the '" + url + "'. Actual error: " + str(sys.exc_info()[0]), 
                                "Rss feed download error")
            if (Emulating): raise
        #xbmcgui.unlock()
    
    def playMedia(self):    
        '''
            Plays the current selected media in the media list.
        '''          
        if (len(self.mediaTrailers) == 0):
            return        
        trailer = self.mediaTrailers[self.listMedia.getSelectedPosition()]
        if (trailer == None):
            return
        
        try:
            streamStr = self.gtWeb.retrieveStreamLinkQuick(trailer)
            if (streamStr <> None):
                xbmc.Player().play(streamStr)
            else:
                self.showMessageBox("There was a problem retrieving the stream URL. Perhaps the GameTrailers.com site has changed.", "Retriving data error")
        except:
            self.showMessageBox("There was a problem playing the media stream, either GameTrailers has changed the media links or the media is not currently available. Actual error: " + str(sys.exc_info()[0]), "Error")
            if (Emulating): raise
        
    def downloadAndPlay(self):    
        '''
            Plays the current selected media in the media list.
        '''          
        if (len(self.mediaTrailers) == 0):
            return        
        trailer = self.mediaTrailers[self.listMedia.getSelectedPosition()]
        if (trailer == None):
            return
        
        try:
            streamStr = self.gtWeb.retrieveStreamLinkQuick(trailer)
            if (streamStr <> None):
                file = self.httpFetcher.urlretrieve(streamStr, None, PATH_ROOT + "temp", "wmv")
                xbmc.Player().play(file)
            else:
                self.showMessageBox("There was a problem retrieving the stream URL. Perhaps the GameTrailers.com site has changed.", "Retriving data error")
        except:
            self.showMessageBox("There was a problem playing the media stream, either GameTrailers has changed the media links or the media is not currently available. Actual error: " + str(sys.exc_info()[0]), "Error")
            if (Emulating): raise
            
    def addMenu(self, text, link, downloadtype):
        '''
            addMenu(string text) -- .
            Adds a menu item to menu list.
            
            text         : The button text.
        '''        
        btn = xbmcgui.ControlButton(MENU_X_POS, self.btnNextYPos, MENU_WIDTH, MENU_HEIGHT, text, PATH_IMAGE + "button-focus.png", PATH_IMAGE + "button-nofocus.png")
        self.addControl(btn)
        btn.setLabel(text, "font12", "0xFF000000", "0xFF000000")
        self.mapMenu[btn.getId()] = MenuItem(text, link, downloadtype)
        if (self.btnTemp <> None):
            btn.controlUp(self.btnTemp)
            self.btnTemp.controlDown(btn)
        btn.controlRight(self.listMedia)
        self.btnTemp = btn
        self.btnNextYPos = self.btnNextYPos + MENU_HEIGHT
        if (self.btnMenuFirst == None):
            self.btnMenuFirst = btn
        self.btnMenuLast = btn
        return btn
    
    def addSubMenu(self, text, link):
        '''
            addSubMenu(string text) -- .
            Adds a sub menu item to menu list.
            
            text         : The button text.
            abbrev       : String that is used when building the rss feed list to retrieve. (Check http://www.gametrailers.com/rss/ for more info)
        '''        
        btn = xbmcgui.ControlButton(MENU_X_POS, self.btnNextYPos, MENU_WIDTH, MENU_SUB_HEIGHT, text, PATH_IMAGE + "button-focus.png", PATH_IMAGE + "button-nofocus.png")
        self.addControl(btn)
        btn.setLabel(text, "font12", "0xFF000000", "0xFF000000")
        self.mapSubMenu[btn.getId()] = MenuItem(text, link)
        if (self.btnTemp <> None):
            btn.controlUp(self.btnTemp)
            self.btnTemp.controlDown(btn)
        btn.controlRight( self.listMedia )
        self.btnTemp = btn
        self.btnNextYPos = self.btnNextYPos + MENU_SUB_HEIGHT
        if (self.btnSubMenuFirst == None):
            self.btnSubMenuFirst = btn
        self.btnSubMenuLast = btn
        return btn
        
    def addInfoLabel(self, text):
        '''
            addMenu(string text) -- .
            Adds a menu item to menu list.
            
            text         : The button text.
        '''        
        lblKey = xbmcgui.ControlLabel(INFO_KEY_X_POS, self.lblInfoNextYPos, INFO_KEY_WIDTH, 10, text, "font13", "0xFF000000")
        self.addControl(lblKey)
        lblValue = xbmcgui.ControlLabel(INFO_VALUE_X_POS, self.lblInfoNextYPos, INFO_VALUE_WIDTH, 10, "", "font13", "0xFF000000")
        self.addControl(lblValue)
        
        self.lblInfoKeys.append(lblKey)
        self.lblInfoValues.append(lblValue)
        self.lblInfoNextYPos = self.lblInfoNextYPos + INFO_HEIGHT
    
    def setSubMenuVisible(self, visible):
        '''
            setSubMenuVisible(boolean visible) -- .
            Hides or shows the sub menu.
            
            visible      : True if the sub menu show be visibled; False otherwise.
        '''           
        xbmcgui.lock()
        if (self.isSubMenuVisible <> visible):
            if (visible):
                self.btnMenuLast.controlDown(self.btnSubMenuFirst)
                self.btnSubMenuFirst.controlUp(self.btnMenuLast)
                self.btnSubMenuLast.controlDown(self.btnMenuFirst)
                self.btnMenuFirst.controlUp(self.btnSubMenuLast)
            else:
                self.btnMenuLast.controlDown(self.btnMenuFirst)
                self.btnMenuFirst.controlUp(self.btnMenuLast)

            self.imgSubMenuBottom.setVisible(visible)
            self.imgSubMenuTop.setVisible(visible)
            self.isSubMenuVisible = visible
            for btnId in self.mapSubMenu.iterkeys():
                if (self.getControl(btnId)<>None):
                    self.getControl(btnId).setVisible(visible)
        xbmcgui.unlock()
    
    def setGameInfoVisible(self, visible):
        '''
            setSubMenuVisible(boolean visible) -- .
            Hides or shows the sub menu.
            
            visible      : True if the sub menu show be visibled; False otherwise.
        '''           
        xbmcgui.lock()
        if (self.isGameInfoVisible <> visible):
            
            for control in self.lblInfoKeys:
                control.setVisible(visible)
            for control in self.lblInfoValues:
                control.setVisible(visible)
            if (self.imgBoxArt <> None):
                self.imgBoxArt.setVisible(visible)
            
            self.isGameInfoVisible = visible
            
            if (visible):                
                #print "setting smaller view"
                self.listMedia.setPosition(290, 85 + 162)
                self.listMedia.setHeight(386 - 162)
            else:
                #print "setting bigger view"
                self.listMedia.setPosition(290, 85)
                self.listMedia.setHeight(386)
        xbmcgui.unlock()

    def setDisplayState(self, newState):
        self.displayState = newState
        if (self.displayState == DISPLAY_GAME):
            self.setGameInfoVisible(True)
        else:
            self.setGameInfoVisible(False)
        

class MenuItem:
    def __init__(self, fullName, linkStr, downloadType = None):
        self.fullName = fullName
        self.linkStr = linkStr
        self.downloadType = downloadType
        #self.isRss = isRss
        
    def getFullName(self):
        return self.fullName
        
    def getLinkStr(self):
        return self.linkStr
