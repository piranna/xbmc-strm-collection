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
import string

def copySeperatedTuple(str, value, seperator = " - "):
    if (value == None):
        return str
    if (len(value) == 0):
        return str
    if (str <> None) and (len(str) > 0):
        return str + seperator + value
    else:
        return value
    
class Game:
    def __init__(self): 
        self.name = None
        self.release = None
        self.platforms = None
        self.publisher = None
        self.developer = None
        self.genres = None
        self.rating = None
        self.guid = None
        self.boxArtLink = None

    def getListStr(self, list):
        str = None
        if (list <> None):
            for item in list:
                str = copySeperatedTuple(str, item.capitalize(), ", ")            
        return str
        
    def getPlatformStr(self):
        return self.getListStr(self.platforms)
    
    def getGenreStr(self):
        return self.getListStr(self.genres)

    def __str__(self):        
        return "[guid=" + str(self.guid) + ", name=" + str(self.name) + ", release=" + str(self.release) + ", publisher=" + \
            str(self.publisher) + ", developer=" + str(self.developer) + ", genres=" + \
            str(self.genres) + ", rating=" + str(self.rating) + ", platforms=" + str(self.getPlatformStr()) + \
            ", boxArtLink=" + str(self.boxArtLink) + "]"
    
    def toString(self):
        str = ""
        if (self.name <> None):
            str = self.name
        if (self.platforms <> None):
            str = str + " - " + self.getPlatformStr()
        return str
    
class Trailer:
    def __init__(self): 
        self.guid = None
        self.gameGuid = None
        self.gameName = None
        self.description = None
        self.title = None
        self.publishedDate = None
        self.thumbnailLink = None
        self.downloadsYesterday = None
        self.downloadsThisWeek = None
        self.downloadsTotal = None
        self.rating = None
        self.externalLink = None
        
    def __str__(self):        
        return "[guid=" + str(self.guid) + ", gameGuid=" + str(self.gameGuid) + ", gameName=" + \
            str(self.gameName) + ", description=" + str(self.description) + ", title=" + \
            str(self.title) + ", date=" + str(self.publishedDate) + ", rating=" + \
            str(self.rating) + ", downloads=" + str(self.downloadsTotal) + " (" + \
            str(self.downloadsYesterday) + " / " + str(self.downloadsThisWeek) + \
            "), thumbLink=" + str(self.thumbnailLink) + " externaLink=" + str(self.externalLink) + "]"

    def toString(self):
        str = self.gameName
        #str = copySeperatedTuple(str, self.guid)        
        str = copySeperatedTuple(str, self.title)
        str = copySeperatedTuple(str, self.description)
        if (self.downloadsYesterday <> None):
            str = copySeperatedTuple(str, "Downloads yesterday: "  + self.downloadsYesterday)
        if (self.downloadsThisWeek <> None):
            str = copySeperatedTuple(str, "Downloads this week: "  + self.downloadsThisWeek)
        if (self.downloadsTotal <> None):
            str = copySeperatedTuple(str, "Total downloads: " + self.downloadsTotal)
        if (self.rating <> None):
            str = copySeperatedTuple(str, "Rating: " + self.rating)
        str = copySeperatedTuple(str, self.publishedDate)
        return str
    
    def copyFromRssItem(self, item):
        self.gameName = str(item.getElement("exInfo:gameName"))
        self.guid = str(item.getElement("guid"))
        self.thumbnailLink = string.replace(item.getElement("exInfo:image"), ' ', '%20')
        
        if (item.hasElement("exInfo:movieTitle")):
            self.title = str(item.getElement("exInfo:movieTitle"))
        if (item.hasElement("description")):
            self.description = str(item.getElement("description"))
        if (item.hasElement("exInfo:downloadsThisWeek")):
            self.downloadsThisWeek = str(item.getElement("exInfo:downloadsThisWeek"))
        if (item.hasElement("exInfo:totalDownloads")):
            self.downloadsTotal = str(item.getElement("exInfo:totalDownloads"))
        if (item.hasElement("rating")):
            self.rating = str(item.getElement("rating"))
        if (item.hasElement("pubDate")):
            self.publishedDate = str(item.getElement("pubDate"))
        if (item.hasElement("exInfo:gameID")):
            self.gameGuid = str(item.getElement("exInfo:gameID"))
