import xml.dom.minidom, urllib, os, os.path, string, traceback, time

# Parser that parses version 2.0 RSS documents
class RSSParser:
    def __init__(self, channelElements, itemElements):
        # Document Object Model of the XML document
        self.dom = None
        # RSS channel information
        self.channelInfo = None
        # RSS items
        self.items = {}
        self.channelElements = channelElements
        self.itemElements = itemElements
                                           
    def reset(self):                                           
        # Document Object Model of the XML document
        self.dom = None
        # RSS channel information
        self.channelInfo = None
        # RSS items
        self.items = {}
    
    # feeds the xml document from given url to the parser
    def feed(self, url):
        self.dom = None
        self.channelInfo = None
        self.items = {}
        f = urllib.urlopen(url)
        xmlDocument = f.read()
        f.close()
        self.dom = xml.dom.minidom.parseString(xmlDocument)
    # feeds the xml document from given url to the parser
    def feedFromFile(self, file):
        self.dom = None
        self.channelInfo = None
        self.items = {}
        try:
            f = open(file)
            xmlDocument = f.read()
        except IOError:
            pass
        f.close()
        self.dom = xml.dom.minidom.parseString(xmlDocument)
    
    # parses the RSS document, for now it assumes that RSS document is valid
    def parse(self):
        self.channelInfo = None
        self.items = {}
        self.channelInfo = self.__parseChannelInfo()
        self.items = self.__parseItems()
    
    # parses channel info and returns RSSChannelInfo object containing the info
    def __parseChannelInfo(self):
        channel = self.dom.getElementsByTagName("channel")[0]
        info = {}
        for channelElement in self.channelElements:
            try:
                info[channelElement] = channel.getElementsByTagName(channelElement)[0].childNodes[0].data
            except IndexError:
                pass
        return RSSChannelInfo(info)
    
    # parses RSS document items and returns an list containing RSSItem objects
    def __parseItems(self):
        items = self.dom.getElementsByTagName("item")
        itemObjects = []
        for item in items:
            elements = {}
            for itemElement in self.itemElements:
                try:
                    elements[itemElement] = item.getElementsByTagName(itemElement)[0].childNodes[0].data
                except IndexError:
                    pass
            itemObjects.append(RSSItem(elements))
        return itemObjects
    
    # returns the channelinfo on this parser
    def getChannelInfo(self):
        return self.channelInfo
    
    # returns items from this parser
    def getItems(self):
        return self.items

class RSSChannelInfo:
    def __init__(self, info):
        # dictionary that includes channel elements
        self.info = info
        
    def getElementNames(self):
        return self.info.keys()
        
    def hasElement(self, element):
        return self.info.has_key(element)
    
    def getElement(self, element):
        return self.info[element]
        
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

class RSSCategory:
    def __init__(self, name, feeds):
        self.name        = name
        self.feeds    = feeds
    
    def getName(self):
        return self.name
        
    def getFeeds(self):
        return self.feeds

class RSSFeed:
    def __init__(self, title, link):
        self.title    = title
        self.link        = link
        
    def getTitle(self):
        return self.title
    
    def getLink(self):
        return self.link