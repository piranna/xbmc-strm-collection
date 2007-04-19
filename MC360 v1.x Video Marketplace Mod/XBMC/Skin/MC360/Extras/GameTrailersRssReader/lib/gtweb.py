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
import xml.dom.minidom, sys, urllib, os, os.path, string, re
import cachedhttp

try:
   reload(gt)
except:
   import gt
   
class GtPage:

    def __init__(self, cachedHttp):
        self.httpFetcher = cachedHttp
        self.gameInfoRegEx = None
        self.gameInfoTextRegEx = None
        self.gameInfoLinkRegEx = None
        self.gameInfoPlatformsRegEx = None
        self.gameInfoNameRegEx = None
        self.gameInfoBoxRegEx = None
        
        self.gameTrailerRegEx = None
        self.gameTrailerInfoRegEx = None
        self.gameTrailerImageLinkRegEx = None

        self.searchRegEx = None
        self.searchGuidRegEx = None
        self.searchNameRegEx = None
        self.searchGenresRegEx = None
        self.searchReleaseRegEx = None
        self.searchBoxRegEx = None
        self.searchPlatRegEx = None
        self.searchPlatTwoRegEx = None

        self.regExPlayer = re.compile('''player.php[^+]*?type=''')
        
        self.regExTrailersWithThumbs = re.compile('''moses/moviesthumbs[^+]*?nowrap''')
        self.regExTrailersWithoutThumbs = re.compile('''<table border="0"id="table9"[^+]*?</table>''')        
        self.regExPageGameNameOne = re.compile('''<a href="gamepage.php?[^+]*?</a''')
        self.regExPageGameNameTwo = re.compile('''>[^+]*?<''')
        self.regExPageGameGuid = re.compile('''gamepage.php[^+]*?" class''')
        self.regExPageTitle = re.compile('''topmedia_sub">[^+]*?</div>''')
        self.regExPageDownloadsTotal = re.compile('''Downloads:[^+]*?</div>''')
        self.regExPageDownloadsYesterday = re.compile('''Yesterday:[^+]*?<b''')
        self.regExPageDescOne = re.compile('''_text[^+]*?</div>''')
        self.regExPageDescTwo = re.compile('''>[^+]*?<''')
        self.regExPageThumbLink = re.compile('''moses/moviesthumb[^+]*?.jpg''')
        self.regExExternalLink = re.compile('''<a target="_blank" href="[^+]*?"''')
        self.regExNumber = re.compile('''[ >][0-9,]*?[< ]''')
        
    def trace(self, str):
        print str
        
    def gameSearch(self, searchStr, platformStr = None, searchPageIndex = 0):
        if (self.searchGuidRegEx == None):
            self.searchGuidRegEx = re.compile('''gamepage.php[^+]*?"><''')
        if (self.searchNameRegEx == None):            
            self.searchNameRegEx = re.compile('''search_title_link[^+]*?</a></div></td''')
        if (self.searchGenresRegEx == None):    
            self.searchGenresRegEx = re.compile('''<b>Genres:</b>[^+]*?</div>''')
        if (self.searchReleaseRegEx == None):    
            self.searchReleaseRegEx = re.compile('''<b>Release Date:</b>[^+]*?</div>''')
        if (self.searchBoxRegEx == None):    
            self.searchBoxRegEx = re.compile('''moses/boxart[^+]*?.jpg''')
        if (self.searchPlatRegEx == None):    
            self.searchPlatRegEx = re.compile('''<b>Platforms:</b>[^+]*?<b>''')
        if (self.searchPlatTwoRegEx == None):    
            self.searchPlatTwoRegEx = re.compile('''[a-zA-Z0-9][^,]*''')
        if (self.searchRegEx == None):    
            self.searchRegEx = re.compile('''<a href="gamepage.php?[^+]*?<div class="search_stats">''')

        # must URL code saerch str
        searchPageLink = "http://www.gametrailers.com/search.php?s=" + searchStr + "&submit_x=0&submit_y=0"
        #if (platformStr <> None):
        #    searchPageLink = searchPageLink + "&p=" + platformStr
        if (searchPageIndex > 0):
            searchPageLink = searchPageLink + "&page=" + str(searchPageIndex * 10)
        
        searchResultStr = self.httpFetcher.urlopen(searchPageLink)
        
        posStart = searchResultStr.find('<div id="showsearch">')
        posStop = searchResultStr.find('<td class="right_shinedark">')
        trailersStr = searchResultStr[posStart:posStop]

        games = []
        
        regMatches = self.searchRegEx.findall(trailersStr)
        for match in regMatches:
            game = gt.Game()
            game.guid = self.searchGuidRegEx.findall(match)[0][21:-3]
            game.name = self.searchNameRegEx.findall(match)[0][48 + len(str(game.guid)):-14]
            game.genres = self.searchGenresRegEx.findall(match)[0][15:-6]
            game.release = self.searchReleaseRegEx.findall(match)[0][21:-6]
            game.boxArtLink = "http://www.gametrailers.com/" + self.searchBoxRegEx.findall(match)[0]
            games.append(game)
            
            platforms = []
            platsStr = self.searchPlatRegEx.findall(match)[0]
            for platStr in self.searchPlatTwoRegEx.findall(platsStr[19:-5]):
                platforms.append(platStr)
            game.platforms = platforms
            
        if (trailersStr.find('&submit_x=0&submit_y=0">Next') <> -1):
            nextSearchPageGames = self.gameSearch(searchStr, platformStr, searchPageIndex + 1)
            games.extend(nextSearchPageGames)
            
        return games
    
    # WORKS
    def retrieveTopTrailers(self, platformStr = None):
        return self.retrieveTrailers("top20", platformStr)
    def retrieveTopRatedTrailers(self, platformStr = None):
        return self.retrieveTrailers("toprated", platformStr)
    def retrieveTopGtTvTrailers(self):
        return self.retrieveTrailers("topgttv", None)
    def retrieveReviewTrailers(self, platformStr = None):
        return self.retrieveTrailers("reviews", platformStr)
    def retrieveE32005Trailers(self, platformStr = None):
        return self.retrieveTrailers("e32k5", platformStr)
    
    # works with special regex
    def retrieveE32006Trailers(self, platformStr = None):
        return self.retrieveTrailers("e32k6", platformStr)    
    
    # does not work
    def retrieveTopUserTrailers(self, platformStr = None):
        return self.retrieveTrailers("umlisting", platformStr)
    def retrieveNewestTrailers(self, platformStr = None):
        return self.retrieveTrailers("newest_noflash", platformStr)
    def retrievePreviewTrailers(self, platformStr = None):
        return self.retrieveTrailers("previews", platformStr)
    
    def retrieveTrailers(self, basePage, platformStr):
        topMediaPageLink = "http://www.gametrailers.com/" + basePage + ".php"
        postData = None
        if (platformStr <> None):
            postData = "p=" + platformStr
        fileStr = self.httpFetcher.urlopen(topMediaPageLink, postData)

        posStart = fileStr.find('<table border="0" cellspacing="0" width="100%"')
        posStop = fileStr.find('<table border="0" cellspacing="0" width="480" cellpadding="0"', posStart)
        trailersStr = fileStr[posStart:posStop]

        trailers = []
        regMatches = self.regExTrailersWithThumbs.findall(trailersStr)
        #regMatches = re.compile('''player.php[^+]*?</table>''').findall(trailersStr)
        for match in regMatches:
            trailer = self.readTrailerFromPage(match)
            trailers.append(trailer)
        regMatches = self.regExTrailersWithoutThumbs.findall(trailersStr)
        for match in regMatches:            
            trailer = self.readTrailerFromPage(match)
            trailers.append(trailer)
        return trailers
    
    def readTrailerFromPage(self, match):
        trailer = gt.Trailer()
        tmpStr = self.regExPageGameNameOne.findall(match)[0]
        trailer.gameName = self.regExPageGameNameTwo.findall(tmpStr)[0][1:-1]
        
        trailer.gameGuid = self.regExPageGameGuid.findall(match)[0][16:-7]

        tmpMatch = self.regExPageTitle.findall(match)
        if (len(tmpMatch) > 0):
            trailer.title = tmpMatch[0][14:-6]

        tmpMatch = self.regExPageDownloadsTotal.findall(match)
        if (len(tmpMatch) > 0):
            trailer.downloadsTotal = self.regExNumber.findall(tmpMatch[0][14:])[0][1:-1]

        tmpMatch = self.regExPageDownloadsYesterday.findall(match)
        if (len(tmpMatch) > 0):
            trailer.downloadsYesterday = self.regExNumber.findall(tmpMatch[0][14:])[0][1:-1]
            
        tmpMatch = self.regExPageDescOne.findall(match)
        if (len(tmpMatch) > 0):
            str = tmpMatch[0]
            tmpMatch = self.regExPageDescTwo.findall(str)
            if (len(tmpMatch) > 0):
                str = tmpMatch[0][1:-1]
            if (len(str) > 0):
                trailer.description = str
        
        tmpMatch = self.regExPageThumbLink.findall(match)
        if (len(tmpMatch) > 0):
            trailer.thumbnailLink = "http://www.gametrailers.com/" + tmpMatch[0]
            
        tmpMatch = self.regExPlayer.findall(match)
        if (len(tmpMatch) > 0):
            trailer.guid = tmpMatch[0][14:-6]
        else:
            trailer.externalLink = self.regExExternalLink.findall(match)[0][25:-1]

        return trailer
    
    
    def retrieveGameInfo(self, gameId):
        if (self.gameInfoRegEx == None):
            self.gameInfoRegEx = re.compile('''<div class="game_data"[^+]*?</div>''')
        if (self.gameInfoNameRegEx == None):
            self.gameInfoNameRegEx = re.compile('''game_title">[^+]*?</div>''')
        if (self.gameInfoPlatformsRegEx == None):
            self.gameInfoPlatformsRegEx = re.compile('''light[^+]*?gif''')
        if (self.gameInfoTextRegEx == None):
            self.gameInfoTextRegEx = re.compile('''> [^+]*?<''')
        if (self.gameInfoLinkRegEx == None):
            self.gameInfoLinkRegEx = re.compile('''link">[^+]*?</a>''')
        if (self.gameInfoBoxRegEx == None):
            self.gameInfoBoxRegEx = re.compile('''http://www.gametrailers.com/moses/boxart[^+]*?.jpg''')
        
        gameInfoPageLink = "http://gametrailers.com/gamepage.php?id=" + str(gameId)
        fileStr = self.httpFetcher.urlopen(gameInfoPageLink)
        regMatches = self.gameInfoRegEx.findall(fileStr)

        gameInfo = gt.Game()
        gameInfo.name = self.gameInfoNameRegEx.findall(fileStr)[0][12:-6]
        gameInfo.guid = str(gameId)
        gameInfo.release = self.gameInfoTextRegEx.findall(regMatches[0])[0][2:-1]
        gameInfo.genres= self.gameInfoTextRegEx.findall(regMatches[5])[0][2:-1]
        gameInfo.rating = self.gameInfoTextRegEx.findall(regMatches[6])[0][2:-1]
        gameInfo.publisher = self.gameInfoLinkRegEx.findall(regMatches[2])[0][6:-4]
        gameInfo.developer = self.gameInfoLinkRegEx.findall(regMatches[3])[0][6:-4]
        gameInfo.boxArtLink = self.gameInfoBoxRegEx.findall(fileStr)[0]

        platforms = []
        for platStr in self.gameInfoPlatformsRegEx.findall(regMatches[1]):
            platforms.append(platStr[6:-4])
        gameInfo.platforms = platforms
        
        return gameInfo
        
    def retrieveGameTrailerList(self, gameId):
        if (self.gameTrailerRegEx == None):
            self.gameTrailerRegEx = re.compile('''src="http://www.gametrailers.com/moses/[^+]*?Downloads</div></td>''')
        if (self.gameTrailerInfoRegEx == None):
            self.gameTrailerInfoRegEx = re.compile('''<div class="media_[^+]*?</div>''')
        if (self.gameTrailerImageLinkRegEx == None):
            self.gameTrailerImageLinkRegEx = re.compile('''http://www.gametrailers.com/moses/moviesthumb[^+]*?.jpg''')
            
        gameInfoPageLink = "http://gametrailers.com/gamepage.php?id=" + str(gameId)
        fileStr = self.httpFetcher.urlopen(gameInfoPageLink)

        posStart = fileStr.find('<!-- MEDIA CONTENT -->')
        posStop = fileStr.find('<!-- END MEDIA CONTENT -->')
        fileStr = fileStr[posStart:posStop]
        regMatches = self.gameTrailerRegEx.findall(fileStr)
        trailerList =  []
        for match in regMatches:
            trailerInfo = gt.Trailer()
            playerMatch = self.regExPlayer.findall(match)
            if (len(playerMatch) > 0):
                trailerInfo.guid = playerMatch[0][14:-6]
                trailerInfo.gameGuid = str(gameId)

                mediaMatches = self.gameTrailerInfoRegEx.findall(match)
                trailerInfo.title = mediaMatches[0][25:-6]
                trailerInfo.description = mediaMatches[3][24:-6]
                trailerInfo.publishedDate = mediaMatches[1][28:-6]
                trailerInfo.downloadsTotal = mediaMatches[4][29:-16]
                
                texts = self.gameTrailerImageLinkRegEx .findall(match)
                if (len(texts) > 0): 
                    trailerInfo.thumbnailLink = texts[0]

                trailerList.append(trailerInfo)        
        return trailerList

    def retrieveStreamLinkQuick(self, trailer):
        if (trailer.externalLink <> None):
            return trailer.externalLink
        else:
            playerPageLink = "http://www.gametrailers.com/player.php?r=1&type=wmv&id=" + str(trailer.guid)
            fileStr = self.httpFetcher.urlopen(playerPageLink)
            regMatches = re.compile('''playNowCall.+;''').findall(fileStr)
            regMatches = re.compile("'.+?'").findall(regMatches[0])
            filenameStr = regMatches[1]
            url = "http://trailers.gametrailers.com/gt_vault/" + filenameStr[1:- 1] + ".wmv"
            return url

    def retrieveStreamStr(self, trailerId):
        try:
            self.trace("Building URL: ")
            playerPageLink = "http://www.gametrailers.com/player.php?r=1&type=wmv&id=" + str(trailerId)
            #print "Player page '" + playerPageLink + "'"        
    
            # Get the player page so we can find out the link to the ad server
            self.trace("Retriving player page: " + str(trailerId))
            self.trace(playerPageLink)
            fileStr = self.httpFetcher.urlopen(playerPageLink)
            # Get the complete stream link from the ad server
            
            self.httpFetcher.setReferer(playerPageLink)
            
            self.trace("Regex matching on player page")
            regMatches = re.compile('''["']http://ad.doubleclick.net/adj/gametrailers.mtvi[^+]*?['"]''').findall(fileStr)
            adServerLink = regMatches[0][1:len(regMatches[0]) - 1]
            
            self.trace("Retriving ad page")
            fileStr = self.httpFetcher.urlopen(adServerLink)
            
            # Get the stream data and parse out the entry tags
            self.trace("Regex macthing on ad page")
            regMatches = re.compile('''["']http://moses.gametrailers.com/streambuilder.php[^+]*?['"]''').findall(fileStr)
            streamLink = regMatches[0][1:len(regMatches[0]) - 1]
            
            self.trace("Retrieving stream page")
            fileStr = self.httpFetcher.urlopen(streamLink)
            
            # Build up a new stream str with only the first two streams
            self.trace("Regex matching on stream page")
            regMatches = re.compile('''<Entry[^+]*?Entry>''').findall(fileStr)
            #asxStreamStr = '<ASX version="3.0">'
            #for link in regMatches[0:2]:
            #    asxStreamStr = asxStreamStr + link
            #asxStreamStr = asxStreamStr + '</ASX>'
            
            return regMatches            
        except:
            print "There was a problem: " + str(sys.exc_info()[0])
            return None
