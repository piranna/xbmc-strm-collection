#################################################################
#                                                               #
#      -=~( TOM GREEN DOT COM THE CHANNEL BROWSER )~=-          #
#                                                               #               
# by InNi < x b m c @ v i s u a l d r u g s . n l > 03-19-2007  #
# Based on the GAN script. thx!                                 #
#                                                               #
#################################################################

#
from string import *
from types import *

import urllib, re, random, string, os.path, htmlentitydefs
import xbmc, xbmcgui

try: Emulating = xbmcgui.Emulating
except: Emulating = False

ACTION_MOVE_LEFT       =  1
ACTION_MOVE_RIGHT      =  2
ACTION_MOVE_UP         =  3
ACTION_MOVE_DOWN       =  4
ACTION_PAGE_UP         =  5
ACTION_PAGE_DOWN       =  6
ACTION_SELECT_ITEM     =  7
ACTION_HIGHLIGHT_ITEM  =  8
ACTION_PARENT_DIR      =  9
ACTION_PREVIOUS_MENU   = 10
ACTION_SHOW_INFO       = 11
ACTION_PAUSE           = 12
ACTION_STOP            = 13
ACTION_NEXT_ITEM       = 14
ACTION_PREV_ITEM       = 15		

######################################################################

RootDir = os.getcwd().replace(";","")+"\\"
if Emulating: 
    RootDir = "./"
ImageDir = RootDir + "images\\"
if Emulating:
    ImageDir = RootDir + "images/"

controller = "true"
#playintro = xbmc.playSFX(RootDir+"intro.wav")
entpat=re.compile("&#?([\w\d]+)[;\s]", re.IGNORECASE)
def HTMLDecode(name): #make titles look nicer in menu
	nameout=''
	lastidx=0
	for match in entpat.finditer(name):
            newchar = '?'
	    try: 
		ent=unichr(int(match.group(1)))
	    except:
	        try: 
		    ent=unichr(htmlentitydefs.name2codepoint[match.group(1)])
                    newchar = ent.encode('iso-8859-1')
	        except:
                    dummy = 0
	    nameout=nameout+name[lastidx:match.start()]+newchar
	    lastidx=match.end()
	nameout=nameout+name[lastidx:]
	nameout=nameout.replace('\xa0',' ') #make nbsp into normal space
	return str(nameout)

def HTMLStrip(text):
    newtext = re.sub('<[^>]*>','',text)
    return newtext


######################################################################
# Generic Stream Browser container classes. 
class GAN:
        urldata = None
        urlheaders = {'User-Agent': 'Mozilla/4.0 (compatible; xbmc-script by iNni; XBMC)', 
                      'Accept-Language': 'en-us',
                     }
        def download(self,url):
            f = urllib.urlopen(url,self.urldata,self.urlheaders)
            data = f.read()
            f.close()
            return data
        
class PageAdapterItem(GAN):
        adapterclass = None
        def __init__(self,title,url,adapter=None):
            # no specified adapter parameter or adapterclass attribute != None means the url points to a stream
            self.title = replace(title, "&amp;", "&")
            self.url = replace(url,"&amp;","&")
            if adapter == None and self.adapterclass != None:
                self.adapter = self.adapterclass(self.title,self.url)
            else:
                self.adapter = adapter
            
        def isStream(self):
            return (self.adapter == None)
        
        def isAdapter(self):
            return not self.isStream()
        
        def getURL(self):                   # override if stream item url should be preprocessed (parsing .asx for instance)
            return self.url                 # normally just returns the provided url
                    
class PageAdapter(GAN):
        regex = '^$'                        # used in matching the url & title of items
        imgregex = None                     # used to find a single image url for this page
        detailregex = None                  # used to find a single detail description for this page
        urlprefix = ''                      # prefix prepended in url matches
        nameprefix = ''                     # prefix prepended in title matches
        imgurlprefix = ''                   # prefix prepended in imgurl matches
        itemclass = PageAdapterItem         # Class type used for items
        
        def __init__(self,title,url):
            self.url = url
            self.title = title
            self.parent = None
            self.items = []
            self.index = None       # index of sub-PageAdapters, or None if parent's index should be used
            self.scroller = ''
            self.image = None
            self.position = 0
	    
            self.isRetrieved = False
            
        def getItem(self, index):
            return self.items[index]

        def hasIndex(self):
            return (self.index != None)
                
        def __iter__(self):
            self.iter_index = 0
            return self
        
        def next(self):
            if self.iter_index < len(self.items):
                self.iter_index = self.iter_index + 1
                return self.items[self.iter_index - 1]
            else:
                raise StopIteration
        
        def setURL(self,url):
            self.url = url
            
        def retrieve(self):
	    print 'retrieving page url : ' + self.url
            if self.isRetrieved:
                return
            self.data = self.download(self.url)
            self.parse()
            self.isRetrieved = True

        def parse(self):
            # for PageAdapter subclasses, provide an easy means to override just the 'regex' attribute without
            # needing to override the parse method. Just redefine 'regex' when subclassing. This default method
            # uses the named regular expression groups 'title' and 'url' (and optionally 'detail' and 'imgurl') 
            # for populating the list of PageAdapterItem objects.
            # For more complex parsing, override this method.
	    cre = re.compile(self.regex, re.DOTALL + re.IGNORECASE)
            result = cre.finditer(self.data)
            for item in result:
                print 'item found : ' + item.group('title')
                newitem = self.itemclass(self.nameprefix + self.processtitle(item.group('title')), self.urlprefix + self.processurl(item.group('url')))
                if newitem.adapter != None:
                    # propagate detail and imgurl to new adapter (when this data cannot be found 
                    # on the next page, but can be found one link earlier)
                    try:
                        newitem.adapter.scroller = self.processdetail(item.group('detail'))
                    except:
                        pass
                    try:
                        newitem.adapter.image = self.processimgurl(item.group('imgurl'))
                    except:
                        pass
                self.items.append(newitem)
                
            if self.imgregex != None:
                cire = re.compile(self.imgregex, re.DOTALL + re.IGNORECASE)
                result = cire.findall(self.data)
		try:
                    self.image = self.processimgurl(self.imgurlprefix + result[0])
                    print "imgurl : " + result[0]
		except:
		    self.image = RootDir + "none.png"
                
            if self.detailregex != None:
                cdre = re.compile(self.detailregex, re.DOTALL + re.IGNORECASE)
                result = cdre.findall(self.data)
		try:
                    self.scroller = self.processdetail(result[0])
		except:
		    self.scroller = 'no detail information found'
		    
		print 'detailinfo : ' + self.scroller
                
                        
        def processtitle(self,text):
            # standard html tag and excessive whitespace remover
            return re.sub('[\n\r]|\s\s+',' ',HTMLStrip(text))
        
        def processurl(self,text):
            return text
        
        def processdetail(self,text):
            # standard html tag and excessive whitespace remover
            return HTMLDecode(re.sub('[\n\r]|\s\s+',' ',HTMLStrip(text)))
        
        def processimgurl(self,text):
            return text  
        
        def toControlList(self, controllist):
            # copy object's itemlist to GUI ControlList
            controllist.reset()
            for item in self.items:
                controllist.addItem(item.title)
		
	    controllist.selectItem(2)
    
	def setSelected(self,pos):
	    self.position = pos
            
######################################################################    
#  Menu          
######################################################################
class MainAdapter(PageAdapter):
        def __init__(self):
            PageAdapter.__init__(self,'Main Menu','')
            self.scroller = 'TomGreen.com The Channel - On Demand Browser'
            self.items = [ PageAdapterItem('Tom Green Live','',tgLiveAdapter()),
            							PageAdapterItem('Poolside Chats with Neil Hamburger','',tgHamburgerAdapter()),
            							PageAdapterItem('Viral Clips','',tgViralAdapter()),
            							PageAdapterItem('Dr. Franklin Ruehl','',tgRuehlAdapter()),
            							PageAdapterItem('Tom\'s Point of View','',tgPofAdapter()),
            							PageAdapterItem('Keepin\' it Real Crew','',tgKircAdapter()),
            							PageAdapterItem('Flippin\' the Switch','',tgFtsAdapter()),
            							PageAdapterItem('Tune into Live Broadcast','',tgLiveLiveAdapter())
                         ]
        def retrieve(self):     # no downloading for this adapter. it's static
            return
        
######################################################################
# * Tom Green LiveLive * 
######################################################################
class tgLiveLiveStream(PageAdapterItem):
        def getURL(self):
            #data = self.download(self.url)
            #result = re.compile('', re.DOTALL + re.IGNORECASE)
            url = 'http://stream.maniatv.com/tomgreenlive'
            return url
#<param name="url" value="http://stream.maniatv.com/tomgreenlive" /><param name='FileName' value='tomgreenTV' />
class tgLiveLiveAdapter(PageAdapter):
        regex = '<param[^<>]*name="url"[^<>]*value="(?P<url>[^<>]*)"[^<>]*(?P<title>.*?)"'
        urlprefix = ''
        itemclass = tgLiveLiveStream
        def __init__(self):
            PageAdapter.__init__(self,'Tom Green Live Broadcast','http://tomgreen.com/')
	    self.scroller = 'Choose the fckd title above to Tune In! Choose the fckd title above to Tune In! Choose the fckd title above to Tune In! '
            
            
######################################################################
# * Tom Green Live * 
######################################################################
class tgLiveStream(PageAdapterItem):
        def getURL(self):
            data = self.download(self.url)
            result = re.compile('download=([^">]+)"', re.DOTALL + re.IGNORECASE)
            url = result.findall(data)
            return url[0]

class tgLiveAdapter(PageAdapter):
        regex = '<a[^<>]*href="(?P<url>[^"]*?)"[^<>]*><b>(?P<title>.*?)</a>'
        urlprefix = 'http://tomgreen.com/ondemand/'
        itemclass = tgLiveStream
        def __init__(self):
            PageAdapter.__init__(self,'Tom Green Live','http://tomgreen.com/ondemand/browser.php?section=1')
	    self.scroller = 'Tom Green Live'
######################################################################




######################################################################
# * Poolside Chats with Neil Hamburger *
######################################################################
class tgHamburgerStream(PageAdapterItem):
        def getURL(self):
            data = self.download(self.url)
            result = re.compile('download=([^">]+)"', re.DOTALL + re.IGNORECASE)
            url = result.findall(data)
            return url[0]

class tgHamburgerAdapter(PageAdapter):
        regex = '<a[^<>]*href="(?P<url>[^"]*?)"[^<>]*><b>(?P<title>.*?)</a>'
        urlprefix = 'http://tomgreen.com/ondemand/'
        itemclass = tgHamburgerStream
        def __init__(self):
            PageAdapter.__init__(self,'Poolside Chats with Neil Hamburger','http://tomgreen.com/ondemand/browser.php?section=5')
	    self.scroller = 'Poolside Chats with Neil Hamburger'
######################################################################




#######################################################################
# * Viral Clips *
######################################################################
class tgViralStream(PageAdapterItem):
        def getURL(self):
            data = self.download(self.url)
            result = re.compile('download=([^">]+)"', re.DOTALL + re.IGNORECASE)
            url = result.findall(data)
            return url[0]

class tgViralAdapter(PageAdapter):
        regex = '<a[^<>]*href="(?P<url>[^"]*?)"[^<>]*><b>(?P<title>.*?)</a>'
        urlprefix = 'http://tomgreen.com/ondemand/'
        itemclass = tgViralStream        
        def __init__(self):
            PageAdapter.__init__(self,'Viral Clips','http://tomgreen.com/ondemand/browser.php?section=6')
	    self.scroller = 'Viral Clips'	    
######################################################################




#######################################################################
# * Dr. Franklin Ruehl *
######################################################################
class tgRuehlStream(PageAdapterItem):
        def getURL(self):
            data = self.download(self.url)
            result = re.compile('download=([^">]+)"', re.DOTALL + re.IGNORECASE)
            url = result.findall(data)
            return url[0]

class tgRuehlAdapter(PageAdapter):
        regex = '<a[^<>]*href="(?P<url>[^"]*?)"[^<>]*><b>(?P<title>.*?)</a>'
        urlprefix = 'http://tomgreen.com/ondemand/'
        itemclass = tgRuehlStream
        def __init__(self):
            PageAdapter.__init__(self,'Dr. Franklin Ruehl','http://tomgreen.com/ondemand/browser.php?section=7')
	    self.scroller = 'Dr. Franklin Ruehl'
######################################################################



#######################################################################
# * Tom's Point of View *
######################################################################
class tgPofStream(PageAdapterItem):
        def getURL(self):
            data = self.download(self.url)
            result = re.compile('download=([^">]+)"', re.DOTALL + re.IGNORECASE)
            url = result.findall(data)
            return url[0]

class tgPofAdapter(PageAdapter):
        regex = '<a[^<>]*href="(?P<url>[^"]*?)"[^<>]*><b>(?P<title>.*?)</a>'
        urlprefix = 'http://tomgreen.com/ondemand/'
        itemclass = tgPofStream
        def __init__(self):
            PageAdapter.__init__(self,'Tom\'s Point of View','http://tomgreen.com/ondemand/browser.php?section=13')
	    self.scroller = 'Tom\'s Point of View'
######################################################################



#######################################################################
# * Keepin' it Real Crew *
######################################################################
class tgKircStream(PageAdapterItem):
        def getURL(self):
            data = self.download(self.url)
            result = re.compile('download=([^">]+)"', re.DOTALL + re.IGNORECASE)
            url = result.findall(data)
            return url[0]

class tgKircAdapter(PageAdapter):
        regex = '<a[^<>]*href="(?P<url>[^"]*?)"[^<>]*><b>(?P<title>.*?)</a>'
        urlprefix = 'http://tomgreen.com/ondemand/'
        itemclass = tgKircStream
        def __init__(self):
            PageAdapter.__init__(self,'Keepin\' it Real Crew','http://tomgreen.com/ondemand/browser.php?section=14')
	    self.scroller = 'Keepin\' it Real Crew'
######################################################################




#######################################################################
# Flippin' the Switch
######################################################################
class tgFtsStream(PageAdapterItem):
        def getURL(self):
            data = self.download(self.url)
            result = re.compile('download=([^">]+)"', re.DOTALL + re.IGNORECASE)
            url = result.findall(data)
            return url[0]

class tgFtsAdapter(PageAdapter):
        regex = '<a[^<>]*href="(?P<url>[^"]*?)"[^<>]*><b>(?P<title>.*?)</a>'
        urlprefix = 'http://tomgreen.com/ondemand/'
        itemclass = tgFtsStream
        def __init__(self):
            PageAdapter.__init__(self,'Flippin\' the Switch','http://tomgreen.com/ondemand/browser.php?section=15')
	    self.scroller = 'Flippin\' the Switch'
######################################################################


class MainWindow(xbmcgui.Window):
        currentAdapter = None

        def __init__(self):
            if Emulating: xbmcgui.Window.__init__(self)

            self.bg = xbmcgui.ControlImage(0,0,0,0, RootDir + "mbg.png")
            self.addControl(self.bg)
            
            self.scroller = xbmcgui.ControlFadeLabel(50, 510, 610, 30, 'font14', '0xAAFFFFFF')
            self.scroller.reset()
            self.addControl(self.scroller)

            self.itemsControlList = xbmcgui.ControlList(80, 140, 570, 360,'font14','0xFF000000')
            self.addControl(self.itemsControlList)
            self.activelist = self.itemsControlList

            self.image = xbmcgui.ControlImage(80,140,180,180, RootDir + "small.png")
            self.addControl(self.image)
            self.image.setVisible(0)

            self.detail = xbmcgui.ControlTextBox(280,140,360,190, 'font13', '0xFF000000')
            self.addControl(self.detail)
            self.detail.setVisible(0)

            self.smallControlList = xbmcgui.ControlList(80, 340, 570, 160,'font14','0xFF000000')
            self.addControl(self.smallControlList)
            self.smallControlList.setVisible(0)

            self.smallControlList.controlRight(self.detail)
            self.smallControlList.controlLeft(self.detail)
            self.detail.controlRight(self.smallControlList)            
            self.detail.controlLeft(self.smallControlList)            
            
            self.title = xbmcgui.ControlLabel(80, 90, 560, 40, "", "font18", "0x60FFFFFF")
            self.addControl(self.title)
	    
            self.mainadapter = MainAdapter()
            self.currentAdapter = self.mainadapter
            self.applyAdapter(self.mainadapter)
            
        ######################################################################
                
        def getImage(self, imageurl):
            print "getting image : " + imageurl
            pe = split(imageurl,'/')
            fname = pe[len(pe)-1]
            fname = re.sub('[^a-zA-Z0-9\.]','',fname)
            if len(fname) > 12:
                fname = fname[len(fname)-12:len(fname)] # to 8.3 filename format
                
            # TODO : check supported extension
            localfname = ImageDir + fname
            print "local name : " + localfname
            if not os.path.exists(localfname):
                try:
                    print "retrieveing image"
                    urllib.urlretrieve((imageurl), (localfname))
                except:
                    print "image retrieve impossible"
                    localfname = RootDir + "none.png"
                    
            self.removeControl(self.image)
            self.image = xbmcgui.ControlImage(80,140,180,180, localfname)
            self.addControl(self.image)
            self.image.setVisible(1)
        
        ######################################################################
                
        def applyAdapter(self, adapter):
            dialog = xbmcgui.Dialog()
                
            self.title.setLabel(adapter.title)
            
            # fire the retrieve method
            try:
                self.activelist.reset()
                self.activelist.addItem("browsing the national internet...")
                if not Emulating:
                    adapter.retrieve()
            except:
                dialog.ok("TomGreen.com","Whaat?! It didnt work.. you may have a connection problem?")
                self.applyAdapter(self.currentAdapter)
                return
                
            if Emulating:
                adapter.retrieve()
                
            if adapter.image == None:
                self.smallControlList.setVisible(0)
                self.image.setVisible(0)
                self.detail.setVisible(0)
                self.itemsControlList.setVisible(1)
                self.activelist = self.itemsControlList
            else:
                self.getImage(adapter.image)
                self.smallControlList.setVisible(1)
                self.image.setVisible(1)
                self.detail.setVisible(1)
                self.itemsControlList.setVisible(0)
                self.activelist = self.smallControlList
            
            # copy items
            adapter.toControlList(self.activelist)
            self.setScroller(adapter.scroller)
            self.setDetail(adapter.scroller)    # to be changed
            # create local reference to current adapter
            self.currentAdapter = adapter
           
            self.setFocus(self.activelist)
	    
	    self.activelist.selectItem(adapter.position)
        
        ######################################################################
                
        def onAction(self, action):
		if action == ACTION_PARENT_DIR:
                        if self.currentAdapter == None:
                            return
                        if self.currentAdapter.parent == None:
                            return
                        self.applyAdapter(self.currentAdapter.parent)
                        
                if action == ACTION_PREVIOUS_MENU:
                        self.close()
                        
        ######################################################################
                        
	def onControl(self, control):
		if control == self.activelist:
                    selectedAdapterItem = self.currentAdapter.items[self.activelist.getSelectedPosition()]
		    # set navpoint
		    self.currentAdapter.setSelected(self.activelist.getSelectedPosition())
                    if selectedAdapterItem.isAdapter():
                        selectedAdapterItem.adapter.parent = self.currentAdapter
                        self.applyAdapter(selectedAdapterItem.adapter)
                    if selectedAdapterItem.isStream():
                        self.playMovie(selectedAdapterItem.getURL())
           
        ######################################################################
            
        def playMovie(self,url):
            print 'playing URL: ' +  url
            try:
                xbmc.Player().play(url)
            except:
                dialog = xbmcgui.Dialog()
                dialog.ok("TomGreen.com","Stream not found. Idunno..")
               
        def setScroller(self,text):
            self.scroller.reset()
            if type(text) is StringType:
                self.scroller.addLabel(text)
            if type(text) is ListType:
                for item in text:
                    self.scroller.addLabel(item)
                
        def setDetail(self,text):
            detailtext = text
            if type(text) is ListType:
                detailtext = join(detailtext)
            self.detail.setText(strip(detailtext))
                
win = MainWindow()
win.doModal()
del win