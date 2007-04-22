#############################################################################
#
#  Comedy Central Video Browser
#  v1.01 by Joshatdot (joshatdot@gmail.com)
#
#  Credit goes to Sander van Grieken
#  I edited his GAN v1.2 script
#
#  Changelog:
#    2006-09-05 Initial Release
#    2006-09-13 GUI changes
#
#############################################################################

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
class CCVB:
        urldata = None
        urlheaders = {'User-Agent': 'Mozilla/4.0 (compatible; CCVB Stream Browser 0.1; XBMC)', 
                      'Accept-Language': 'en-us',
                     }
        def download(self,url):
            f = urllib.urlopen(url,self.urldata,self.urlheaders)
            data = f.read()
            f.close()
            return data
        
class PageAdapterItem(CCVB):
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
                    
class PageAdapter(CCVB):
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
            
    
#            
######################################################################
# 
class MainAdapter(PageAdapter):
        def __init__(self):
            PageAdapter.__init__(self,'Comedy Central Video Browser v1.0','')
            self.scroller = 'Comedy Central Video Browser - Main Index Page'
            self.items = [ PageAdapterItem('All Access: Middle Ages','',AllAccessAdapter()),
                           PageAdapterItem('Blue Collar Comedy Tour','',BlueCollarAdapter()),
                           PageAdapterItem('Chappelle Show','',ChappelleAdapter()),
                           PageAdapterItem('The Colbert Report','',ColbertReportAdapter()),
                           PageAdapterItem('Comedians of Comedy','',ComediansAdapter()),
                           PageAdapterItem('Comedy Central Movies','',MoviesAdapter()),
                           PageAdapterItem('Comedy Central Presents','',PresentsAdapter()),
                           PageAdapterItem('Roast of Jeff Foxworthy','',FoxworthyAdapter()),
                           PageAdapterItem('Roast of Pamela Anderson','',AndersonAdapter()),
                           PageAdapterItem('Roast of William Shatner','',ShatnerAdapter()),
                           PageAdapterItem('Roast: Denis Leary','',LearyAdapter()),
                           PageAdapterItem('Con','',ConAdapter()),
                           PageAdapterItem('Crank Yankers','',YankersAdapter()),
                           PageAdapterItem('The Daily Show With Jon Stewart','',DailyShowAdapter()),
                           PageAdapterItem('Denis Learys Merry Fuckin Christmas Special','',Leary2Adapter()),
                           PageAdapterItem('Distraction','',DistractionAdapter()),
                           PageAdapterItem('Dog Bites Man','',DogAdapter()),
                           PageAdapterItem('Dr. Katz Professional Therapist','',KatzAdapter()),
                           PageAdapterItem('Drawn Together','',DrawnAdapter()),
                           PageAdapterItem('Galaxy of the Black Stars','',GalaxyAdapter()),
                           PageAdapterItem('Golden Age','',GoldenAgeAdapter()),
                           PageAdapterItem('Drew Careys Green Screen Show','',CareyAdapter()),
                           PageAdapterItem('The Hollow Men','',HollowAdapter()),
                           PageAdapterItem('I Love the 30s','',Love30sAdapter()),
                           PageAdapterItem('Insomniac Special','',InsomniacSpecialAdapter()),
                           PageAdapterItem('Insomniac With Dave Attell','',DaveAttellAdapter()),
                           PageAdapterItem('Jump Cuts','',JumpCutsAdapter()),
                           PageAdapterItem('Kid Notorious','',KidNotoriousAdapter()),
                           PageAdapterItem('Last Laugh 2005','',LastLaugh2005Adapter()),
                           PageAdapterItem('Live at Gotham','',LiveatGothamAdapter()),
                           PageAdapterItem('Mind of Mencia','',MindofMenciaAdapter()),
                           PageAdapterItem('Premium Blend','',PremiumBlendAdapter()),
                           PageAdapterItem('Primetime Glick','',PrimetimeGlickAdapter()),
                           PageAdapterItem('RENO 911','',RENO911Adapter()),
                           PageAdapterItem('Shorties Watchin Shorties','',ShortiesAdapter()),
                           PageAdapterItem('Showbiz Show','',ShowbizShowAdapter()),
                           PageAdapterItem('South Park','',SouthParkAdapter()),
                           PageAdapterItem('Stella','',StellaAdapter()),
                           PageAdapterItem('Strangers With Candy','',StrangersAdapter()),
                           PageAdapterItem('Test Pilots','',TestPilotsAdapter()),
                           PageAdapterItem('Thats My Bush','',ThatsMyBushAdapter()),
                           PageAdapterItem('Tiny Hands','',TinyHandsAdapter()),
                           PageAdapterItem('Too Late with Adam Carolla','',CarollaAdapter()),
                           PageAdapterItem('Trigger Happy TV','',TriggerHappyTVAdapter()),
                           PageAdapterItem('TV Funhouse','',TVFunhouseAdapter()),
                           PageAdapterItem('Upright Citizens Brigade','',UCBAdapter()),
                           PageAdapterItem('Wanda Does It','',WandaDoesItAdapter()),
                           PageAdapterItem('Wanderlust','',WanderlustAdapter()),
                           PageAdapterItem('Weekends at the DL','',WeekendsAdapter()),
                           PageAdapterItem('Odd Todd','',OddToddAdapter()),
                           PageAdapterItem('Shadow Rock','',ShadowRockAdapter()),
                           PageAdapterItem('The Clip Joint','',TheClipJointAdapter())
                         ]
        def retrieve(self):     # no downloading for this adapter. it's static
            return
        
#            
######################################################################
# 
     
class DailyShowStream(PageAdapterItem):
        def getURL(self):
            data = self.download(self.url)
            result = re.compile('<input[^<>]+value="([^">]+)"', re.DOTALL + re.IGNORECASE)
            url = result.findall(data)
            data = self.download(url[0])
            result = re.compile('<ref\s+href="(mms\:[^"]+)"', re.DOTALL + re.IGNORECASE)
            url = result.findall(data)
            return url[0]
        
class DailyShowAdapter(PageAdapter):
        regex = '<a[^<>]*href="(?P<url>play\.jhtml[^<>"]+)"[^<>]*>(?P<title>[^\n]+)</a>'
        urlprefix = 'http://www.comedycentral.com/sitewide/media_player/'
        itemclass = DailyShowStream
        def __init__(self):
            PageAdapter.__init__(self,'The Daily Show with Jon Stewart','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=934')
	    self.scroller = 'The Daily Show with Jon Stewart'

#
#######################################################################
#

class AllAccessAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'All Access: Middle Ages','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=61092')
		self.scroller = 'All Access: Middle Ages'

class BlueCollarAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Blue Collar Comedy Tour','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=63792')
		self.scroller = 'Blue Collar Comedy Tour'

class ChappelleAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Chappelle Show','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=936')
		self.scroller = 'Chappelle Show'

class ColbertReportAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'The Colbert Report','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=18252')
		self.scroller = 'The Colbert Report'

class ComediansAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Comedians of Comedy','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=24456')
		self.scroller = 'Comedians of Comedy'

class MoviesAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Comedy Central Movies','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=16629')
		self.scroller = 'Comedy Central Movies'

class PresentsAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Comedy Central Presents','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=931')
		self.scroller = 'Comedy Central Presents'

class FoxworthyAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Roast of Jeff Foxworthy','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=930')
		self.scroller = 'Roast of Jeff Foxworthy'

class AndersonAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Roast of Pamela Anderson','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=16194')
		self.scroller = 'Roast of Pamela Anderson'

class ShatnerAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Roast of William Shatner','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=70867')
		self.scroller = 'Roast of William Shatner'

class LearyAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Roast: Denis Leary','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=15171')
		self.scroller = 'Roast: Denis Leary'

class ConAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Con','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=929')
		self.scroller = 'Con'

class YankersAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Crank Yankers','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=928')
		self.scroller = 'Crank Yankers'

class Leary2Adapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Denis Learys Merry Fuckin Christmas Special','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=24795')
		self.scroller = 'Denis Learys Merry Fuckin Christmas Special'

class DistractionAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Distraction','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=927')
		self.scroller = 'Distraction'

class DogAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Dog Bites Man','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=68819')
		self.scroller = 'Dog Bites Man'

class KatzAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Dr. Katz Professional Therapist','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=61884')
		self.scroller = 'Dr. Katz Professional Therapist'

class DrawnAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Drawn Together','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=932')
		self.scroller = 'Drawn Together'

class GalaxyAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Galaxy of the Black Stars','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=55082')
		self.scroller = 'Galaxy of the Black Stars'

class GoldenAgeAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Golden Age','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=63830')
		self.scroller = 'Golden Age'

class CareyAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Drew Careys Green Screen Show','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=18056')
		self.scroller = 'Drew Careys Green Screen Show'

class HollowAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'The Hollow Men','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=926')
		self.scroller = 'The Hollow Men'

class Love30sAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'I Love the 30s','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=68905')
		self.scroller = 'I Love the 30s'

class InsomniacSpecialAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Insomniac Special','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=17218')
		self.scroller = 'Insomniac Special'

class DaveAttellAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Insomniac With Dave Attell','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=925')
		self.scroller = 'Insomniac With Dave Attell'

class JumpCutsAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Jump Cuts','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=17384')
		self.scroller = 'Jump Cuts'

class KidNotoriousAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Kid Notorious','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=17514')
		self.scroller = 'Kid Notorious'

class LastLaugh2005Adapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Last Laugh 2005','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=24970')
		self.scroller = 'Last Laugh 2005'

class LiveatGothamAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Live at Gotham','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=60735')
		self.scroller = 'Live at Gotham'

class MindofMenciaAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Mind of Mencia','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=15463')
		self.scroller = 'Mind of Mencia'

class PremiumBlendAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Premium Blend','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=923')
		self.scroller = 'Premium Blend'

class PrimetimeGlickAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Primetime Glick','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=16051')
		self.scroller = 'Primetime Glick'

class RENO911Adapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'RENO 911','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=935')
		self.scroller = 'RENO 911'

class ShortiesAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Shorties Watchin Shorties','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=922')
		self.scroller = 'Shorties Watchin Shorties'

class ShowbizShowAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Showbiz Show','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=17199')
		self.scroller = 'Showbiz Show'

class SouthParkAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'South Park','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=933')
		self.scroller = 'South Park'

class StellaAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Stella','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=15187')
		self.scroller = 'Stella'

class StrangersAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Strangers With Candy','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=61976')
		self.scroller = 'Strangers With Candy'

class TestPilotsAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Test Pilots','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=60343')
		self.scroller = 'Test Pilots'

class ThatsMyBushAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Thats My Bush','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=17852')
		self.scroller = 'Thats My Bush'

class TinyHandsAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Tiny Hands','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=63805')
		self.scroller = 'Tiny Hands'

class CarollaAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Too Late with Adam Carolla','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=16111')
		self.scroller = 'Too Late with Adam Carolla'

class TriggerHappyTVAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Trigger Happy TV','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=16797')
		self.scroller = 'Trigger Happy TV'

class TVFunhouseAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'TV Funhouse','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=17721')
		self.scroller = 'TV Funhouse'

class UCBAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Upright Citizens Brigade','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=61907')
		self.scroller = 'Upright Citizens Brigade'

class WandaDoesItAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Wanda Does It','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=921')
		self.scroller = 'Wanda Does It'

class WanderlustAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Wanderlust','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=17386')
		self.scroller = 'Wanderlust'

class WeekendsAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Weekends at the DL','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=16053')
		self.scroller = 'Weekends at the DL'

class OddToddAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Odd Todd','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=69944')
		self.scroller = 'Odd Todd'

class ShadowRockAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'Shadow Rock','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=69497')
		self.scroller = 'Shadow Rock'

class TheClipJointAdapter(DailyShowAdapter):
	def __init__(self):
		PageAdapter.__init__(self,'The Clip Joint','http://www.comedycentral.com/sitewide/media_player/browseresults.jhtml?showId=70150')
		self.scroller = 'The Clip Joint'

#            
######################################################################
######################################################################

class MainWindow(xbmcgui.Window):
        currentAdapter = None

        def __init__(self):
            if Emulating: xbmcgui.Window.__init__(self)

            # background animation
            self.imgBackgroundani = xbmcgui.ControlImage(0, 0, 720, 476, "Q:\\skin\\MC360\\Extras\\background-ani.gif")
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
            self.vislabel           = xbmcgui.ControlLabel(145,443,375,20,'Full Screen Visualization','font12','0xFFFFFFFF')
            self.backlabel           = xbmcgui.ControlLabel(580,423,80,20,'Back','font12','0xFFFFFFFF')
            self.selectlabel           = xbmcgui.ControlLabel(577,443,80,20,'Select','font12','0xFFFFFFFF')

            self.addControl(self.medialabel) 
            self.addControl(self.vislabel)
            self.addControl(self.backlabel)
            self.addControl(self.selectlabel)

            self.title = xbmcgui.ControlLabel(90, 30, 576, 40, "", "font18", "0xFFFFFFFF")
            self.addControl(self.title)
	    
            self.itemsControlList = xbmcgui.ControlList(92, 64, 578, 385,'font14','0xFF000000')
            self.addControl(self.itemsControlList)
            self.activelist = self.itemsControlList

            self.image = xbmcgui.ControlImage(72, 140, 180, 180, RootDir + "small.png")
            self.addControl(self.image)
            self.image.setVisible(0)

            self.detail = xbmcgui.ControlTextBox(280, 140, 360, 190, 'font13', '0xFFFFFFFF')
            self.addControl(self.detail)
            self.detail.setVisible(0)

            self.smallControlList = xbmcgui.ControlList(72, 340, 570, 160,'font14','0xFF000000')
            self.addControl(self.smallControlList)
            self.smallControlList.setVisible(0)

            self.smallControlList.controlRight(self.detail)
            self.smallControlList.controlLeft(self.detail)
            self.detail.controlRight(self.smallControlList)            
            self.detail.controlLeft(self.smallControlList)            
            
            self.scroller = xbmcgui.ControlFadeLabel(72, 432, 576, 30, 'font13', '0xE0AAAAFF')
            self.scroller.reset()
            self.addControl(self.scroller)

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
                self.activelist.addItem("downloading. please wait...")
                if not Emulating:
                    adapter.retrieve()
            except:
                dialog.ok("Comedy Central Script","Could not retrieve online information.")
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
            #self.setScroller(adapter.scroller)
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
                dialog.ok("Comedy Central","Stream not found.")
               
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
