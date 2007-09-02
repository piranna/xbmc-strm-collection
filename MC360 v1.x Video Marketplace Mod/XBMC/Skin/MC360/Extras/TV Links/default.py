import xbmc, xbmcgui
import os
import sys
import urllib
import time
import re
import socket
import string

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

ROOT_DIR = os.getcwd()[:-1]+'\\'
IMAGE_DIR = ROOT_DIR+'images\\'

dialogProgress = xbmcgui.DialogProgress()

#############################################################################
# autoscaling values
#############################################################################

HDTV_1080i = 0      #(1920x1080, 16:9, pixels are 1:1)
HDTV_720p = 1       #(1280x720, 16:9, pixels are 1:1)
HDTV_480p_4x3 = 2   #(720x480, 4:3, pixels are 4320:4739)
HDTV_480p_16x9 = 3  #(720x480, 16:9, pixels are 5760:4739)
NTSC_4x3 = 4        #(720x480, 4:3, pixels are 4320:4739)
NTSC_16x9 = 5       #(720x480, 16:9, pixels are 5760:4739)
PAL_4x3 = 6         #(720x576, 4:3, pixels are 128:117)
PAL_16x9 = 7        #(720x576, 16:9, pixels are 512:351)
PAL60_4x3 = 8       #(720x480, 4:3, pixels are 4320:4739)
PAL60_16x9 = 9      #(720x480, 16:9, pixels are 5760:4739)

#############################################################################

class TVLink(xbmcgui.Window):
	def __init__(self):
		try:
			self.setCoordinateResolution(PAL_4x3)
			self.Cats = ["Shows", "Cartoons", "Documentaries", "Anime", "Movies", "Music Videos"]
			self.Links = ["http://www.tv-links.co.uk/index.do/1", "http://www.tv-links.co.uk/index.do/2", "http://www.tv-links.co.uk/index.do/9", "http://www.tv-links.co.uk/index.do/3", "http://www.tv-links.co.uk/index.do/4", "http://www.tv-links.co.uk/index.do/5",]
			self.ctrlBackGround = xbmcgui.ControlImage(0, 0, 720,576, IMAGE_DIR + 'background.png')
			self.ctrlLogo = xbmcgui.ControlImage(30, 5, 50, 100, IMAGE_DIR + 'logo.png')
			self.addControl(self.ctrlBackGround)
			self.addControl(self.ctrlLogo)
			self.ctrlList = xbmcgui.ControlList(205, 130, 500, 400, font='font14',textColor='0xFFFFFFFF', buttonFocusTexture=IMAGE_DIR + 'focus.png', itemTextXOffset=-7, itemTextYOffset=-2, itemHeight=15)
			self.addControl(self.ctrlList)
			self.lblPage = xbmcgui.ControlLabel(100, 75, 455, 500, 'test', 'font14','0xFFFFFFFF')
			self.addControl(self.lblPage)
			self.ctrlList.reset()
			self.makeButtons()
			self.ctrlList.controlLeft(self.btnCategories[0])
			self.prev = ""
			self.prevs = ""
			self.pages = ["", "", "", ""]
			self.curcat = 0
			self.pages[0] = self.Cats[0]
			self.do_page()
			self.get_list(self.Links[0])
			for z in sorted(self.list):
				self.page = 1
				self.ctrlList.addItem(xbmcgui.ListItem(label=z))
			self.setFocus(self.ctrlList)
			#self.addControl(xbmcgui.ControlImage(90, 3, 60, 60,ROOT_DIR + 'default.tbn'))
		except Exception, e:
			dialog = xbmcgui.Dialog()
			dialog.ok("Error", "Error initializing script.\n\nReason:\n"+str(e))

	
	def do_page(self):
		try:
			if self.pages[0] != "":
				self.lblPage.setLabel(self.pages[0])
				if self.pages[1] != "":
					self.lblPage.setLabel(self.pages[0]+" > "+self.pages[1])
					if self.pages[2] != "":
						self.lblPage.setLabel(self.pages[0]+" > "+self.pages[2])
						if self.pages[3] != "":
							self.lblPage.setLabel(self.pages[0]+" > "+self.pages[2]+" > "+self.pages[3])
		except Exception, e:
			dialog = xbmcgui.Dialog()
			dialog.ok("Error", "Error printing selected path.\n\nReason:\n"+str(e))

	def getCategory(self):
		try:
			if self.pages[2] != "":
				name=self.pages[2]
				if self.pages[3] != "":
					name=self.pages[2]+", "+self.pages[3]
			return name
		except Exception, e:
			dialog = xbmcgui.Dialog()
			dialog.ok("Error", "Playlist could not be opened.\n\nReason:\n"+str(e))
			return ""


	def get_list(self, url):
		try:
			self.list = {}
			sock = urllib.urlopen(url)
			htmlSource = sock.read()
			sock.close()
			reCAT = re.compile('<div class="ctr"><em id="letter">(.+?)</em></div>\n\s+</div>\n\s+</div>\n\s+</div>\n\s+<ul>(.+?)</ul>', re.DOTALL)
			reLIST = re.compile('<a href="/listings/(.+?)">(.+?)</a>', re.DOTALL)
			list = {}
			for i in reCAT.finditer(htmlSource):
				links = {}
				for x in reLIST.finditer(i.group(2)):
					links[x.group(2)] = 'http://www.tv-links.co.uk/listings/' + x.group(1)
				list[i.group(1)] = links
			self.list = list
		except Exception, e:
			dialog = xbmcgui.Dialog()
			dialog.ok("Error", "Playlist could not be opened.\n\nReason:\n"+str(e))

	
	def get_eps(self, url):
		try:
			self.list = {}
			self.morder = {}
			sock = urllib.urlopen(url)
			htmlSource = sock.read()
			sock.close()
			reEP = re.compile('<h4>(.+?)</h4>\n\s+<table cellspacing="0" cellpadding="2" border="0">(.+?)</table>', re.DOTALL)
			reSINGEP = re.compile('<tr>\n\s+<td>\n\s+(.+?)\s\n\s+</td>\n\s+<td>(.+?)</td>.+?</tr>', re.DOTALL)
			reSINGEPNAME = re.compile('<a target="_blank" href="(.+?)" onclick=".+?">(.+?)</a>', re.DOTALL)
			rePART = re.compile('^Part \d', re.DOTALL)
			last = "";
			for i in reEP.finditer(htmlSource):
				links = {}
				a = 0
				order = {}
				for x in reSINGEP.finditer(i.group(2)):
					for y in reSINGEPNAME.finditer(x.group(2)):
						name = y.group(2)
						if rePART.search(name):
							name = last+" "+name
						else:
							last = y.group(2)
						order[a] = x.group(1)+" "+name
						a = a+1
						links[x.group(1)+" "+name] = 'http://www2.tv-links.co.uk'+y.group(1)
				self.list[i.group(1)] = links
				self.morder[i.group(1)] = order
		except Exception, e:
				dialog = xbmcgui.Dialog()
				dialog.ok("Error", "Unable to look up episodes.\n\nReason:\n"+str(e))

	def get_link(self, url):
		link = ""
		try:
			#dialog = xbmcgui.Dialog()
			#dialog.ok("Error", url)
			sock = urllib.urlopen(url)
			htmlSource = sock.read()
			sock.close()
			reDIVX = re.compile('http://www([0-9]?)\.tv-links\.co\.uk/video/(.+?)\.divx', re.DOTALL)
			reFLV = re.compile('videoFile: \'(.+?)\'', re.DOTALL)
			reSWF = re.compile('<embed type="application/x-shockwave-flash" src="(.+?)"', re.DOTALL)
			divx = reDIVX.search(htmlSource)
			flv = reFLV.search(htmlSource)
			swf = reSWF.search(htmlSource)
			if divx:
				#dialog = xbmcgui.Dialog()
				#dialog.ok("DIVX1", str(divx)+"\n"+link)
				link = "http://www2.tv-links.co.uk/video/"+divx.group(2)+".divx"
				#dialog = xbmcgui.Dialog()
				#dialog.ok("DIVX2", str(divx)+"\n"+link)
			elif flv:
				#dialog = xbmcgui.Dialog()
				#dialog.ok("FLV", str(flv)+"\n"+link)
				link = flv.group(1)
			elif swf:
				#dialog = xbmcgui.Dialog()
				#dialog.ok("SWF", str(swf)+"\n"+link)
				link = swf.group(1)
			mySocket = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
			mySocket.connect ( ( 'www2.tv-links.co.uk', 80 ) )
			mySocket.send ( "GET "+link+" HTTP/1.1\r\nHost: www2.tv-links.co.uk\r\nUser-Agent: Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.4) Gecko/20070515 Firefox/2.0.0.4\r\nAccept: text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5\r\nAccept-Language: en-us,en;q=0.5\r\nAccept-Encoding: gzip,deflate\r\nAccept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7\r\nKeep-Alive: 300\r\nConnection: keep-alive\r\n\r\n" )
			htmlSource = mySocket.recv ( 1000 )
			mySocket.close()
			#dialog = xbmcgui.Dialog()
			#dialog.ok("Antwort", str(htmlSource))
			#print "link:"+link
			#print "url:"+url
			#print "src:"+htmlSource
			reLOC = re.compile("Location: (.+?)\r\n", re.DOTALL)
			LOC = reLOC.search(htmlSource)
			if LOC:
				link = LOC.group(1)
			if swf:
				reGUBA = re.compile('http://www\.guba\.com/f/root\.swf\?isEmbeddedPlayer=false&bid=(.+?)$', re.DOTALL)
				reDM = re.compile('http%3A%2F%2Fwww\.dailymotion\.com%2Fget%2F14%2F320x240%2Fflv%2F(.+?)%3Fkey%3D(.+?)&prev', re.DOTALL)
				reGOOGLE = re.compile('http://video\.google\.com/googleplayer\.swf\?.+?%3Fversion%3D(.+?)%26secureurl%3D(.+?)%26', re.DOTALL)
				GUBA = reGUBA.search(link)
				DM = reDM.search(link)
				GOOGLE = reGOOGLE.search(link)
				if GUBA:
					resubGUBA = re.compile('^(\d).+?$', re.DOTALL)
					subGUBA = resubGUBA.search(GUBA.group(1))
					num = int(subGUBA.group(1)) - 1
					link = "http://free.guba.com/download/flash/1/"+str(num)+"/"+GUBA.group(1)+"/"
				elif DM:
					link = "http://www.dailymotion.com/get/14/320x240/flv/"+DM.group(1)+"?key="+DM.group(2)+""
				elif GOOGLE:
					link = "http://vp.video.google.com/videodownload?version="+GOOGLE.group(1)+"&secureurl="+GOOGLE.group(2)
		except Exception, e:
				dialog = xbmcgui.Dialog()
				dialog.ok("Error", "Playlist could not be opened.\n\nReason:\n"+str(e))
		return link
		
	def makeButtons(self):
		try:
			self.btnCategories = []
			for i in range(len(self.Cats)):
				btn = xbmcgui.ControlButton(25, (130)+27*i, (247)-((100))+20, 27, self.Cats[i],textXOffset=30, focusTexture=IMAGE_DIR + self.Cats[i]+'NF'+'.png', noFocusTexture=IMAGE_DIR + self.Cats[i]+'NF'+'.png', textColor='0xFFAAAAAA',focusedColor='0xFFFFFFFF')
				self.addControl(btn)
				self.btnCategories.append(btn)

			for i in range(len(self.Cats)):
				self.btnCategories[i].controlUp(self.btnCategories[i-1])
				self.btnCategories[i].controlDown(self.btnCategories[(i+1) % len(self.Cats)])
				self.btnCategories[i].controlRight(self.ctrlList)
		except Exception, e:
			dialog = xbmcgui.Dialog()
			dialog.ok("Error", "Error creating buttons.\n\nReason:\n"+str(e))
			
	def onAction(self, action):
		try:
			if action == ACTION_PARENT_DIR:
				if self.page >= 2:
					if self.page == 2:
						self.page = 1
						self.ctrlList.reset()
						self.pages[1] = ""
						self.do_page()
						for z in sorted(self.list):
							self.ctrlList.addItem(xbmcgui.ListItem(label=z))
					elif self.page == 3:
						dialogProgress.create("Downloading", "Getting list for "+self.Cats[self.curcat]+".")
						self.get_list(self.Links[self.curcat])
						dialogProgress.close()
						self.page = 2
						self.ctrlList.reset()
						self.pages[2] = ""
						self.do_page()
						for z in sorted(self.list[self.prev]):
							self.ctrlList.addItem(xbmcgui.ListItem(label=z))
					elif self.page == 4:
						self.page = 3
						self.ctrlList.reset()
						self.pages[3] = ""
						self.do_page()
						for y in sorted(self.list):
							self.ctrlList.addItem(xbmcgui.ListItem(label=y))
			if action == ACTION_PREVIOUS_MENU:
	                    self.close()
			if ((action == ACTION_SHOW_INFO) or (action==ACTION_CONTEXT_MENU)):
				if self.page == 4:
					try:
						dialog = xbmcgui.Dialog()
						fn = dialog.browse(3, 'Save Video to...', 'files')
						item = self.ctrlList.getSelectedItem()
					except Exception, e:
						return
					if not os.path.isdir(fn):
						return
					dialogProgress.create("Downloading", "Getting video url for "+item.getLabel()+".")
					vidlink = self.get_link(self.list[self.prevs][self.morder[self.prevs][self.ctrlList.getSelectedPosition()]])
					dialogProgress.close()
					name=self.getCategory()+", "+item.getLabel()
					fname=self.secureFileName(name)
					if (vidlink.find("divx")>0):
						fext=".divx"
					else:
						fext=".flv"
					fnum=""
					c=0
					while (os.path.exists(fn+fname+fnum+fext)):
						c=c+1
						fnum=str(c)
					self.save(vidlink,fn+fname+fnum+fext,name)
					dialog = xbmcgui.Dialog()
					answer=dialog.yesno("Download successful", "Successfully saved the video to:",fn+fname+fnum+fext,"Do you want to play the video now?")
					if (answer):
						play=xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
						play.clear()
						play.add(fn+fname+fnum+fext,self.getCategory()+", "+item.getLabel()+" (TVLinks)")
						xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(play)
		except Exception, e:
			dialog = xbmcgui.Dialog()
			dialog.ok("Error", "Error in onAction.\n\nReason:\n"+str(e))

	def hook(self,count_blocks, block_size, total_size):
		current_size = block_size * count_blocks
		value = current_size * 100 / total_size
		self.downloadDialog.update(value)

	def save(self,url,destination,name):
		self.downloadDialog = xbmcgui.DialogProgress()
		self.downloadDialog.create("Downloading","Downloading "+name+"\nURL: "+url+"\nDestination: "+destination)
		try:
			DL=urllib.urlretrieve( url , destination , self.hook)
			self.downloadDialog.close()
		except Exception,e:
			self.downloadDialog.close()
			dialog = xbmcgui.Dialog()
			dialog.ok("Error", "Error downloading.\n\nReason:\n"+str(e))

	def secureFileName(self,name):
		goodName=""
		for i in range( len(name) ):
			if (self.isGoodChar(name[i])):
				goodName+=name[i]
		return goodName[0:30]
	
	def isGoodChar(self,char):
		return (char in string.ascii_letters+string.digits)
			
	def onControl(self, control):
		try:
			if control == self.ctrlList:
				if self.page == 1:
					self.page = 2
					item = self.ctrlList.getSelectedItem()
					self.ctrlList.reset()
					self.prev = item.getLabel()
					self.pages[1] = item.getLabel()
					self.do_page()
					for y in sorted(self.list[item.getLabel()]):
						self.ctrlList.addItem(xbmcgui.ListItem(label=y))
				elif self.page == 2:
					self.page = 3
					item = self.ctrlList.getSelectedItem()
					dialogProgress.create("Downloading2", "Getting list for "+item.getLabel()+".")
					self.get_eps(self.list[self.prev][item.getLabel()])
					self.ctrlList.reset()
					self.pages[2] = item.getLabel()
					self.do_page()
					for y in sorted(self.list):
						self.ctrlList.addItem(xbmcgui.ListItem(label=y))
					dialogProgress.close()
				elif self.page == 3:
					self.page = 4
					item = self.ctrlList.getSelectedItem()
					self.prevs = item.getLabel()
					self.ctrlList.reset()
					self.pages[3] = item.getLabel()
					self.do_page()
					for y in self.morder[item.getLabel()]:
						self.ctrlList.addItem(xbmcgui.ListItem(label=self.morder[item.getLabel()][y]))
				elif self.page == 4:
					item = self.ctrlList.getSelectedItem()
					#print(self.list[self.prevs][self.morder[self.prevs][self.ctrlList.getSelectedPosition()]])
					dialogProgress.create("Downloading", "Getting video url for "+item.getLabel()+".")
					vidlink = self.get_link(self.list[self.prevs][self.morder[self.prevs][self.ctrlList.getSelectedPosition()]])
					dialogProgress.close()
					#xbmcgui.Dialog().ok('READY', "LINK: "+vidlink)
					play=xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
					play.clear()
					play.add(vidlink,self.getCategory()+", "+item.getLabel()+" (TVLinks)")
					xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(play)
					#dialog = xbmcgui.Dialog()
					#dialog.ok("Error", vidlink+"\n"+self.getCategory()+", "+item.getLabel()+" (TVLinks)")
					#xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(vidlink)
					#print("LINK: "+vidlink)
			else:
				for i in range(len(self.Cats)):
					if control == self.btnCategories[i]:
						self.curcat = i
						self.pages = [self.Cats[self.curcat], "", "", ""]
						self.do_page()
						dialogProgress.create("Downloading", "Getting list for "+self.Cats[i]+".")
						self.ctrlList.reset()
						### CurCat Icon ###
						#self.addControl(xbmcgui.ControlImage(20, 85, 77, 97,IMAGE_DIR + self.Cats[i]+'.png'))
						###################
						self.get_list(self.Links[i])
						for z in sorted(self.list):
							self.page = 1
							self.ctrlList.addItem(xbmcgui.ListItem(label=z))
						dialogProgress.close()
		except Exception, e:
				dialog = xbmcgui.Dialog()
				dialog.ok("Error", "Error in onControl.\n\nReason:\n"+str(e))

try:
	window = TVLink()
	window.doModal()
	del window
except Exception, e:
	dialog = xbmcgui.Dialog()
	dialog.ok("Error", "Error running script.\n\nReason:\n"+str(e))

