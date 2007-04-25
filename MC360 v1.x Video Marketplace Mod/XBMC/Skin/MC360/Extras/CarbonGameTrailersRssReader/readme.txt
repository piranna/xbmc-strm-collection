GameTrailersRSSReader.py - RSS Reader from GameTrailers.com RSS Feeds
    
    With this script it is possible to watch game trailers on your XBox,
    courtesy of GameTrailers.com. The script will download the RSS feeds
    from GT, and display them with descriptions and thumbnails. It can
    also parse the GT web pages and return review list, top rated and most
    downloaded trailers.
    With the search feature, it is possible to search for any game and see 
    all trailers for that game.
    
    This is my first xbmc script (and python) so bare with me if you find
    any bugs. Please report all bugs to me so I can fix them in the next 
    release. Unfortunately I was a little late for E3 2006, but at least 
    now it is possible to stream from GT again.

Installation and usage:
        Copy the GameTrailersRSSReader folder to the xbmc scripts folder.
        Start the script and select one of the feeds (newest, top 20, top 
        rated) and watch the trailers.

        To see the game page for a trailer, mark the trailer and press Info.
        To show the context menu, mark a trailer and press Title.

Changelog:
        0.4.2 (14th february 2007):
            Fixed backgruond image resize issues in other resolutions than PAL 4x3
            Fixed issue when script restarted when it was stopped
        0.4.1 (5 february 2007):
            Fixed broken parsing
            Updated to follow guidelines for www.xbmcscripts.com
        0.4 (2 june 2006):
            Added parsing of the GT webpages since most of the RSS feeds wasnt
              updated very often.
            Added search functionality, now it is possible to search for any game.
            Added "Download & Play" so you can download the trailer before
              playing it. It will take a while to download the trailer but
              it will not freeze during playback because buffering.
            Added Game information for a trailer. Now you can view information
              about the any game and see all trailers for it.
            Put all python script files into lib except the main script
            Fixed a thumbnail for the main script.
        0.3 (18 may 2006):
            Find out the actual name of the trailer instead of relying on
              the name of the thumbnail. Now all trailers should work.
        0.2 (14 may 2006):
            Fixed the trailer problem by streaming to the actual wmv file directly.
        0.1 (13 may 2006):
            First version with PAL 4:3 support only
            
Known issues:
        Layout issues in other TV formats. I need help with GUI layouts for 
          other display formats than PAL 4:3, please send me source patches for 
          other formats if they are needed.
        Currently there is no Nintendo Wii RSS feed, so it is not possible to
          get the latest trailers for the platform.
        Some trailers has no thumbnail. The GT web pages will most of the time
          only show thumbnails for the first five trailers.

Todo:
        Add the Nintendo Wii RSS feed (GT has no specific feed for this 
          platform yet)
        Fix layouts for widescreen, ntsc and all other formats out there. 
          If you can test and fix it for me, send me the source on how to 
          fix it. I can't do anything here.
        Add videos ad support so gametrailers.com wont lose any income because
          of this script. Hey, its free and it should be kept that way!
            
Other script resources that has been used to create this script:
        The following scripts were used in order to create this script, 
        some parts from them may be copied and re-used in this script. I would 
        like to thank you those who made the scripts. To get the real versions 
        of the scripts, visit www.xbmcscripts.com.
        
        cachedhttp.py v1.3 script - Script created by Aslak Grinsted. Script 
          copied as a seperate file.
        rss.py v1.5 - RSS logic copied from Multi RSS Reader created by Affini - 
          aka Aaron . Script copied into a seperate file.
        aftonbladet.py v2.01 - The seperate dialog window was copied from the 
          Aftonbladet XBMC script created by Anders Willstedt..

Support:
    For bugs/enhancements/ideas/etc go to http://xbmc.ramfelt.se
    
License:
	GNU General Public License.
	TV.com XBMC script is free software; you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation; either version 2 of the License, or
	(at your option) any later version.
	
	TV.com XBMC is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.
	
	You should have received a copy of the GNU General Public License
	along with TV.com XBMC; if not, write to the Free Software
	Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
        
Last words:
        Have fun!