#
# coding: utf-8
#
# Retro-X:  v1.01 (Primary Release).
# (-) = Todo    (*) = Done
# Highlighted Changes:                                          Change Notes:
# ----------------------------------------------------------------------------------------
# (*) Language Key for A Button.                                -- LANGUAGE[6]
# (*) Favourites Dialog: change from yes/no to OK.              
# (*) Change Dialog message "Auto Return Is: (On)"
#     for options.                                              -- LANGUAGE[55],[56],[57],[58]
# (*) Automatic selecting of the default.tbn if
#     it exists in the same dir as the xbe.                     -- Will check only if icon left blank.
# (*) hide ROM extensions, Add as an option to System Config.   -- LANGUAGE[8] key updated.
# (*) Configure selectable sound packs from System Config.      -- LANGUAGE[10] key Updated.
#                                                                  new directory 'sound' added.
# (*) Modify button labels to turn off when showing dialogs     -- Implemented for Clearity Skin
# (*) Create Skin for Clearity                                  -- skins/CLGUI.xml
# (*) Create Skin for BlackBolt Classic                         -- skins/BBGUI.xml
# (*) Create Skin for X-Tv                                      -- skins/XTGUI.xml
# (*) Config removed from Install to allow for easier updating.
# (*) Create small procedure to remove some old files if exist.
#

import  os, xbmc, xbmcgui, sys, string, threading,time,traceback
from    copy        import deepcopy

global  PYSCRIPT
PYSCRIPT    =   ''

def Debug(self):
    self.Emu_Thread.terminate()   
    self.close()

try:
    Emulating = xbmcgui.Emulating
except:
    Emulating = False

## Constants (NO NEED TO CHANGE)
VERSION         =   '1.01'                                  # version of Retro-X.
HOME_DIR        =   os.getcwd().replace(";","")+"\\"        # get homedirectory for the script
SKINS	        =   HOME_DIR    +   'skins\\'               # Path to Skins Directory
GUIMD           =   HOME_DIR    +   'media'                 # Path to Images/Graphics
LIBS            =   HOME_DIR    +   'libs\\'                # Path to Libraries.
SOUND           =   HOME_DIR    +   'sound\\'               # Path To Sound Files
LANGDIR         =   HOME_DIR    +   'language\\'            # Path to language strings
GAMEDIR         =   HOME_DIR    +   'games\\'               # Path to save game lists to.
CFGXML          =   HOME_DIR    +   'config.xml'            # Path to config.xml for this script.
GUIXML          =   'Q:\\UserData\\guisettings.xml'         # Path to xbmc guisettings.xml
SRCXML          =   'Q:\\UserData\\sources.xml'             # Path to xbmc sources.xml
CUT_FILE        =   "launch.cut"                            # Name of file to call emulator + game               
sys.path.append(LIBS)                                       # Append LIBS directory to search path.

## Pre-Check for Update:
if os.path.isfile(CFGXML)               :
    if os.path.isfile(HOME_DIR + 'guibuilder.py')   :   os.remove(HOME_DIR + 'guibuilder.py')
    if os.path.isfile(HOME_DIR + 'emuos.py')        :   os.remove(HOME_DIR + 'emuos.py')    


## States, used for onaction to know where it was called from
STATE_EMU       =   int(1)                                  # Viewing Emulators
STATE_ROMS      =   int(2)                                  # Viewing Rom
STATE_FAVES     =   int(3)                                  # Viewing All Favourites

## Button Codes
ACTION_MOVE_LEFT        =  1
ACTION_MOVE_RIGHT       =  2
ACTION_MOVE_UP          =  3
ACTION_MOVE_DOWN        =  4
ACTION_PAGE_UP          =  5
ACTION_PAGE_DOWN        =  6
ACTION_SELECT_ITEM      =  7
ACTION_HIGHLIGHT_ITEM   =  8
ACTION_B                =  9
ACTION_PREVIOUS_MENU    = 10
ACTION_SHOW_INFO        = 11
ACTION_PAUSE            = 12
ACTION_STOP             = 13
ACTION_NEXT_ITEM        = 111
ACTION_PREV_ITEM        = 112
ACTION_Y                = 34
ACTION_X                = 18

## Check that the extra core module is present... ##
CORE = True
try     :   import core
except  :   CORE = False


LANGOK,LANGUAGE = core.Check_Lang(LANGDIR,GUIXML)
XBMC_SKIN       = core.GetATag('skin',GUIXML)                    

class Launcher(xbmcgui.Window):
    def __init__(self):
        self.setCoordinateResolution(6)
        if Emulating: xbmcgui.Window.__init__(self)
                
        #Initialize lists
        self.ViewState  =   int(0)      # Current Display
        self.Emus       =   {}          
        self.Conf       =   {}
        self.Auto       =   {}
        self.Sounds     =   {}
        self.index      =   ''
        self.Subidx     =   0
        self.ClearList()
        self.cfg = {'title':7,'emupath':21,'icon':23,'name':46,'rompath':22,'romext':24,'picpath':35,'picformat':42,'artpath':47,'flatten':85}

        ## Get Config Data..If null then re-create it..
        self.Conf           =   core.GetAllTags('system',CFGXML)
        if len(self.Conf)   ==  0           :
            self.Conf['Auto']               =   {}
            self.Conf['Auto']['SOUND']      =   'default'
            self.Conf['Auto']['DOAUTO']     =   1
            self.Conf['Auto']['DUALDISP']   =   1
            self.Conf['Auto']['SHOWEXT']    =   1             

        self.Auto       =   self.Conf['Auto']

        if not self.Auto.has_key('SHOWEXT') :   self.Auto['SHOWEXT']    =   1           # Add ShowEXt Key if not exist..
        if not self.Auto.has_key('SOUND')   :   self.SetSounds()
        else                                :   self.SetSounds(self.Auto['SOUND'])
                 
        self.Emus       =   core.GetAllTags('emulator',CFGXML)
        
        self.SFX(self.Sounds['start'])
                
        self.DisplayVars('--- self.Emus ---',self.Emus)
        self.DisplayVars('--- self.Auto ---',self.Auto)
        
        # Load Skin..
        self.SUCCEEDED  =   False
        import guibuilder
        self.icon_emu = ''
        SkinDict    =   {'MC360':'MCGUI.xml','Clearity':'CLGUI.xml','Blackbolt Classic':'BBGUI.xml','xTV':'XTGUI.xml'}
        if SkinDict.has_key(XBMC_SKIN)  :
            guibuilder.GUIBuilder(self,SKINS + SkinDict[XBMC_SKIN],GUIMD,title='Retro-X - Loading',debug=True)
        else                            :
            guibuilder.GUIBuilder(self,SKINS + 'DFGUI.xml',GUIMD,title='Retro-X - Loading',debug=True)
        if      self.SUCCEEDED          :   pass # OK Continue
        else                            :   self.close()
       
        self.ButtonLabel(10,'A',True,LANGUAGE[6])
        
        self.controls[4]['control'].setLabel(LANGUAGE[41])
        self.controls[5]['control'].setLabel(LANGUAGE[11])
        self.controls[6]['control'].setLabel(LANGUAGE[12])
        self.controls[7]['control'].setLabel(LANGUAGE[60])
        
        if self.Auto.has_key('exec_use')    :   
            self.Autoexec('READ')
            self.SaveCfg()
            self.setFocus(self.controls[50]['control'])
            
        if      self.index == ''        :   self.ShowEmus(Init=True)
        elif    self.index == 'FAVES'   :   self.ShowFaves(Init=True)
        else                            :   self.ShowRoms(self.index,Init=True)

        self.Emu_Thread = EmuThread(self)               
        self.Emu_Thread.start()


    def SetSounds(self,theme='default') :
        self.Sounds         =   {}
        self.Auto['SOUND']  =   theme
        snddir              =   SOUND + theme +'\\'
        for item in ['move','start','end','select','launch','faves','dialog']    :
            if os.path.isfile(snddir + item +'.wav')    :   self.Sounds[item]   =   snddir + item +'.wav'
            else                                        :   self.Sounds[item]   =   ''

        
    def SFX(self,sound)     :
        if sound != ''      :   xbmc.playSFX(sound)


    def ClearList(self) :
        self.romListItem    =   []  # ListItem data..
        self.Dir            =   []  # Directory Info..
        self.Rom            =   []  # Rom Name..
        self.Ext            =   []  # Ext Name..
        self.Plays          =   []  # Number of Plays..
        self.PicInfo        =   []  # Picture Information..
        self.FavesSub       =   []  # Favourites subindex..

        
    def DisplayVars(self,TheText,TheVars):
        print str(TheText)
        for k,v in TheVars.iteritems()  :   print '-- '+ str(k) +': '+ str(v)


    def AppendReturn(self,pyfile)   :
        try :
            f       =   open(pyfile,"a+")
            data    =   f.readlines()
            Found   =   False
            for i in range(-1,-6,-1):
                if 'Emureturn.py'   in  data[i]  :   Found = True
            if not (Found)          :
                f.write('\n\n\n')
                f.write('import xbmc\n')
                f.write('xbmc.executescript(\"'+ HOME_DIR + 'Emureturn.py' +'\")\n')
            f.close()
            f       =   open(HOME_DIR + 'emuflag.chk',"wb")
            f.close()
        except  :
            f.close()
            traceback.print_exc()
            Debug(self)

        
    def Autoexec(self,doaction):
        try:
            print '--Autoexec'
            if doaction == 'READ':
                del self.Auto['exec_use']                
                if self.Auto.has_key('exec_exist')              :              
                    os.remove('q:\\scripts\\autoexec.py')
                    os.rename(self.Auto['exec_exist'],'q:\\scripts\\autoexec.py')
                    del self.Auto['exec_exist']          
                else:
                    os.remove('q:\\scripts\\autoexec.py')
                if self.Auto.has_key('exec_splash')             :        
                    os.rename(self.Auto['exec_splash'],'q:\\media\\splash.png')            
                    del self.Auto['exec_splash']
                if self.Auto.has_key('exec_emu')                :
                    self.index  =    self.Auto['exec_emu']
                    del self.Auto['exec_emu']
                else:
                    self.index  =   ''
            else:   ### doaction passed must have been 'WRITE'
                self.Auto['exec_use']             =   'Run'
                if os.path.isfile('q:\\scripts\\autoexec.py'):
                    self.Auto['exec_exist']       =   'q:\\scripts\\autoexec_EMU.py'
                    os.rename('q:\\scripts\\autoexec.py',self.Auto['exec_exist'])
                if os.path.isfile('q:\\media\\splash.png'):
                    self.Auto['exec_splash']      =   'q:\\media\\splash_EMU.png'
                    os.rename('q:\\media\\splash.png',self.Auto['exec_splash'])
                if self.Emus[self.index]['type'] != 'emugame'   :   self.Auto['exec_emu']   =   ''
                elif self.ViewState              == STATE_FAVES :   self.Auto['exec_emu']   =   'FAVES'
                else                                            :   self.Auto['exec_emu']   =   self.index               
                ### Create new autoexec.py...
                f=open('q:\\scripts\\autoexec.py',"wb")
                f.write('import xbmc\n')
                f.write('xbmc.executescript(\"'+ HOME_DIR + '\\default.py' +'\")')
                f.close()
        except:
            traceback.print_exc()
            Debug(self)


    def SaveCfg(self):
        try:
            core.PutConfig({'emulator':self.Emus,'system':self.Conf},CFGXML)
            if self.index != '' and self.ViewState == STATE_ROMS    :
                self.PutGames(self.filehash)
        except:
            traceback.print_exc() 
            Debug(self)

        
    def DelEmu(self):
        try:
            print '--DelEmu'
            self.SFX(self.Sounds['dialog'])
            EMUS    =   self.Emus.keys()
            EMUS.sort()
            result = xbmcgui.Dialog().select(LANGUAGE[12],EMUS)
            if result != -1 :    ## User canceled remove operation
                answer = EMUS[result]
                if xbmcgui.Dialog().yesno(LANGUAGE[12],LANGUAGE[15],str(answer)):                
                    del self.Emus[EMUS[result]]
                    self.ShowEmus()
        except:
            traceback.print_exc() 
            Debug(self)
    

    def AddEmu(self):
        try:
            print '--AddEmu'
            ### Prompt for type of EMU to add
            self.SFX(self.Sounds['dialog'])
            options     = [LANGUAGE[70],LANGUAGE[71],LANGUAGE[72],LANGUAGE[73]]
            result      = xbmcgui.Dialog().select(LANGUAGE[45],options)
            modarr      = {}
            if      result  ==   0  :   modarr['type'] = 'emugame'
            elif    result  ==   1  :   modarr['type'] = 'emualone'
            elif    result  ==   2  :   modarr['type'] = 'homebrew'
            elif    result  ==   3  :   modarr['type'] = 'python'
            else                    :   return                    
            Status,modarr   =   self.ConfMenu(modarr)
            if Status   == True     :
                NewTitle            =   modarr.pop('title')
                self.Emus[NewTitle] =   {}
                self.Emus[NewTitle].update(modarr)
            self.ShowEmus()
        except:
            traceback.print_exc()
            Debug(self)


    def ModEmu(self):
        try:
            print '--ModEmu'
            self.SFX(self.Sounds['dialog'])
            EMUS    =   self.Emus.keys()
            EMUS.sort()
            result = xbmcgui.Dialog().select(LANGUAGE[41],EMUS)
            if result == -1 :    ## User canceled remove operation
                pass
            else:
                OrigTitle       =   EMUS[result]
                modarr          =   deepcopy(self.Emus[OrigTitle])
                modarr['title'] =   OrigTitle
                self.DisplayVars('-- modarr:',modarr)
                Status,modarr   =   self.ConfMenu(modarr)                
                if Status   == True  :
                    ClearIt = False
                    if modarr['type'] == 'emugame'  :
                        if modarr['rompath'][0] != self.Emus[OrigTitle]['rompath'][0]   :   ClearIt = True
                        if not self.Emus[OrigTitle].has_key('flatten')      : self.Emus[OrigTitle]['flatten'] = {}
                        if not self.Emus[OrigTitle]['flatten'].has_key(0)   : self.Emus[OrigTitle]['flatten'][0] = 0
                        if modarr['flatten'][0] != self.Emus[OrigTitle]['flatten'][0]   :   ClearIt = True                        
                    NewTitle        =   modarr.pop('title')
                    del self.Emus[OrigTitle]
                    self.Emus[NewTitle] =   {}
                    self.Emus[NewTitle].update(modarr)
                    self.DisplayVars('---- Self.Emus ENDED :',self.Emus[NewTitle])
                    if ClearIt  :   self.ClearCache(NewTitle,0)
                self.ShowEmus()
        except:
            traceback.print_exc()
            Debug(self)
            

    def ConfMenu(self,modarr,Indx=-1):
        try:
            print '--ConfMenu'
            if      modarr['type']  !=  'emugame': ItemList = ['title','emupath','icon']
            elif    Indx            ==  -1       : ItemList = ['title','emupath','icon','name','rompath','romext','picpath','picformat','artpath','flatten']
            else                                 : ItemList = ['name','rompath','picpath','artpath','flatten']
            if      Indx == -1   :   Indx = 0
            Status      = False
            GuiDone     = False
            while GuiDone == False:
                modlist  =  []  # Clear array for dialog select.
                Opt      =  []
                for Item in ItemList    :
                    if Item == 'name' or Item == 'rompath' or Item == 'picpath' or Item == 'artpath' or Item == 'flatten':
                        if not modarr.has_key(Item)             :   modarr[Item]    =   {}
                        if not modarr[Item].has_key(Indx)       :
                            if Item == 'flatten'                :   modarr[Item][Indx]  =   0
                            else                                :   modarr[Item][Indx] =   LANGUAGE[27]
                        if Item == 'flatten' : modlist.append(LANGUAGE[self.cfg[Item]] + ' ['+ str(bool(int(modarr[Item][Indx]))) +']')
                        else                 : modlist.append(LANGUAGE[self.cfg[Item]] + ' ['+ modarr[Item][Indx] +']')
                    else                                                                                :
                        if not modarr.has_key(Item)             :   modarr[Item]    =   LANGUAGE[27]
                        modlist.append(LANGUAGE[self.cfg[Item]] + ' ['+ modarr[Item] +']')
                    Opt.append(Item)
                modlist.append(LANGUAGE[28])                                                # OK Button
                Opt.append(LANGUAGE[28])
                modlist.append(LANGUAGE[29])                                                # Cancel Button..
                Opt.append(LANGUAGE[29])
                choice = xbmcgui.Dialog().select(LANGUAGE[0],modlist)                       # Display select menu

                if      choice == -1 or Opt[choice] == LANGUAGE[29] :   GuiDone = True ;  Status = False
                else    :
                    if      Opt[choice] == 'title'     : modarr['title']         = self.KeyText(modarr['title'],LANGUAGE[30])
                    elif    Opt[choice] == 'emupath'   : modarr['emupath']       = xbmcgui.Dialog().browse(1,LANGUAGE[31],'files') 
                    elif    Opt[choice] == 'icon'      : modarr['icon']          = xbmcgui.Dialog().browse(2,LANGUAGE[33],'files')
                    elif    Opt[choice] == 'name'      : modarr['name'][Indx]    = self.KeyText(modarr['name'][Indx],LANGUAGE[46]) 
                    elif    Opt[choice] == 'rompath'   : modarr['rompath'][Indx] = xbmcgui.Dialog().browse(0,LANGUAGE[32],'files') 
                    elif    Opt[choice] == 'flatten'   :
                        if not modarr['flatten'].has_key(Indx)  :   modarr['flatten'][Indx] = 0
                        else                                    :   modarr['flatten'][Indx] = self.ToggleVar(modarr['flatten'][Indx]) 
                    elif    Opt[choice] == 'romext'    : modarr['romext']        = self.KeyText(modarr['romext'],LANGUAGE[34])  
                    elif    Opt[choice] == 'picpath'   : modarr['picpath'][Indx] = xbmcgui.Dialog().browse(0,LANGUAGE[37],'files')
                    elif    Opt[choice] == 'picformat' : modarr['picformat']     = self.KeyText(modarr['picformat'],LANGUAGE[43])                 
                    elif    Opt[choice] == 'artpath'   : modarr['artpath'][Indx] = xbmcgui.Dialog().browse(0,LANGUAGE[37],'files')
                    else                               : Status,GuiDone,modarr   = self.CheckInput(modarr,ItemList,Idx=Indx)
                    
            return Status,modarr
        except:
            traceback.print_exc()
            Debug(self)


    def KeyText(self,txt,hdr):
        try:
            print '--KeyText'
            KEYBOARD = xbmc.Keyboard(txt,hdr)
            KEYBOARD.doModal()
            if (KEYBOARD.isConfirmed()):
                keystring = KEYBOARD.getText()
            else        :
                keystring = ''
            del KEYBOARD
            return keystring
        except:
            del KEYBOARD
            traceback.print_exc()
            Debug(self)

            
    def CheckInput(self,modarr,ItemList,Idx=0):
        try :
            print '--CheckInput'
            HowMany     =   len(ItemList)
            print '-- Vars to Check: '+ str(HowMany)
            for Item in ItemList :
                Ok  =   False
                if      Item    ==  'title'     :   Ok,modarr[Item]       = self.CheckAVar(modarr[Item],'text')
                elif    Item    ==  'emupath'   :   Ok,modarr[Item]       = self.CheckAVar(modarr[Item],'exe',Ext=modarr['type'])
                elif    Item    ==  'icon'      :   Ok,modarr[Item]       = self.CheckAVar(modarr[Item],'pic',Ext=modarr['emupath'])
                elif    Item    ==  'name'      :   Ok,modarr[Item][Idx]  = self.CheckAVar(modarr[Item][Idx],'text')
                elif    Item    ==  'rompath'   :   Ok,modarr[Item][Idx]  = self.CheckAVar(modarr[Item][Idx],'path')
                elif    Item    ==  'romext'    :   Ok,modarr[Item]       = self.CheckAVar(modarr[Item],'text')
                elif    Item    ==  'picpath'   :   Ok,modarr[Item][Idx]  = self.CheckAVar(modarr[Item][Idx],'path',CanBeNull=True)
                elif    Item    ==  'picformat' :   Ok,modarr[Item]       = self.CheckAVar(modarr[Item],'text',CanBeNull=True)
                elif    Item    ==  'artpath'   :   Ok,modarr[Item][Idx]  = self.CheckAVar(modarr[Item][Idx],'path',CanBeNull=True)
                else                            :
                    print '--Ignored: '+ str(Item)
                    Ok = True
                if Ok                           :   HowMany = HowMany - 1
                print '--Item: '+ str(Item) +' Var:'+ str(modarr[Item]) +' Status:'+ str(Ok) +' Vars Left:'+ str(HowMany)
            if      HowMany >= 1    :   return False,False,modarr
            else                    :   return True,True,modarr
        except:
            traceback.print_exc()
            Debug(self)
            

    def CheckAVar(self,Var,Type,CanBeNull=False,Ext='') :
        try :
            print '--CheckAVar Var:'+ str(Var) +' Type:'+ str(Type) +' Null:'+ str(CanBeNull) +' Emutype:'+ str(Ext)
            if      Type == 'text'  :
                if      (Var == '' or Var == LANGUAGE[27]) and (not CanBeNull)  :   return False,Var  
                elif    (Var == '' or Var == LANGUAGE[27]) and (CanBeNull)      :   return True,''
                else                                                            :   return True,Var
            elif    Type == 'path'  :
                if      (Var == '' or Var == LANGUAGE[27]) and (not CanBeNull)  :   return False,Var                
                elif    (Var == '' or Var == LANGUAGE[27]) and (CanBeNull)      :   return True,''
                else                                                            :
                    if  Var[-1:] !=  '\\'                                       :   return True,Var + '\\'
                    else                                                        :   return True,Var
            elif    Type == 'exe'   :
                if      Ext == 'python' : Ext = '.py'
                else                    : Ext = 'xbe'
                if      Var == '' or Var == LANGUAGE[27]                        :   return False,Var
                else                                                            :
                    if  Var[-3:].lower() != Ext.lower()                         :   return False,Var
                    else                                                        :   return True,Var
            elif    Type == 'pic'   :
                if      Var == '' or Var == LANGUAGE[27]                        :
                    if not os.path.isfile(os.path.dirname(Ext) +'\\default.tbn'):   return False,Var
                    else                                                        :   return True,Var
                else                                                            :   return True,Var
            else                                                                :   return False,Var           
        except:
            traceback.print_exc()
            Debug(self)
        

    def CtlButtons(self,State)   :
        try:
            self.controls[4]['control'].setVisible(State)
            self.controls[5]['control'].setVisible(State)
            self.controls[6]['control'].setVisible(State)
            self.controls[7]['control'].setVisible(State)
        except:
            traceback.print_exc()
            Debug(self)


    def NavButtons(self,State)  :
        try:
            for ButtId in [10,11,12,13,14,15,16,17] :
                self.controls[ButtId]['control'].setVisible(State)
        except:
            traceback.print_exc()
            Debug(self)
        

    def DualDisplay(self,State) :
        try:
            self.controls[95]['control'].setVisible(State)
            if State == True    :
                if self.ViewState == STATE_FAVES    :   self.controls[96]['control'].setImage('')
                else                                :   self.controls[96]['control'].setImage(self.Emus[self.index]['icon'])
            self.controls[96]['control'].setVisible(State)        
        except:
            traceback.print_exc()
            Debug(self)


    def ButtonLabel(self,ButtId,ButtAl,State,ButtTxt)  :
        try:
            if State == True    :   ButtonImg = GUIMD + '\\button-'+ ButtAl +'.png'
            else                :   ButtonImg = GUIMD + '\\button-'+ ButtAl +'-turnedoff.png'
            self.controls[ButtId]['control'].setImage(ButtonImg)
            self.controls[ButtId+1]['control'].setLabel(ButtTxt)
        except:
            traceback.print_exc()
            Debug(self)

                
    def RomLabel(self,MyLabel):
        self.controls[40]['control'].setLabel(str(MyLabel))


    def ShowEmus(self,Init=False):
        try:
            print '--ShowEmus'
            if Init == False    :   self.SFX(self.Sounds['select'])
            self.ViewState = STATE_EMU
            self.index = ''
            self.controls[50]['control'].reset()

            if bool(int(self.Auto['DUALDISP'])) == True :
                self.DualDisplay(False)            
                self.CtlButtons(True)
            else    :
                self.DualDisplay(False)
                self.CtlButtons(True)
            
            self.ButtonLabel(12,'B',True,LANGUAGE[1])
            self.ButtonLabel(14,'X',True,LANGUAGE[86])
            self.ButtonLabel(16,'Y',False,'')
            
            self.RomLabel('')
            
            self.ClearList()    #   Clear all the Info..
            
            self.controls[20]['control'].setLabel(str(len(self.Emus))+' '+LANGUAGE[9])
            EMU = self.Emus.keys()
            if len(EMU) ==  0   :
                xbmcgui.Dialog().ok(LANGUAGE[63],LANGUAGE[64])
            else                :
                EMU.sort()
                for emu in EMU:
                    if self.Emus[emu]['type'] == 'emugame'  :   label2    =   ''
                    else                                    :   label2    =   LANGUAGE[62]
                    self.controls[50]['control'].addItem(xbmcgui.ListItem(emu,label2,iconImage=self.icon_emu))
                self.setFocus(self.controls[50]['control'])
        except:
            traceback.print_exc()
            Debug(self)


    def ShowRoms(self,indx,Source=-1,Faves=[],Init=False):
        try:
            print '--ShowRoms'
            if Init == False    :   self.SFX(self.Sounds['select'])
            self.index      = indx
            self.controls[50]['control'].reset()
            self.ViewState  = STATE_ROMS

            if bool(int(self.Auto['DUALDISP'])) == True :
                self.CtlButtons(False)
                self.DualDisplay(True)
            else    :
                self.DualDisplay(False)
                self.CtlButtons(True)
            
            self.ButtonLabel(12,'B',True,LANGUAGE[4])
            self.ButtonLabel(14,'X',True,LANGUAGE[44])
            self.ButtonLabel(16,'Y',True,LANGUAGE[53])

            ## Check for the default view of the Emulator
            if Source == -1 :
                if self.Emus[self.index].has_key('view')    :   self.Subidx     =   int(self.Emus[self.index]['view'])
                else                                        :   self.Subidx     =   0
            else                                            :   self.Subidx     =   Source

            ## Display Emulator and Name of Source being viewed..
            self.RomLabel(str(self.index) +' / '+ str(self.Emus[self.index]['name'][self.Subidx]))

            ## Set Variables for Pictures.
            picf,picok,artok,picidx,artidx = self.CheckPics(self.index,self.Subidx,False,False,False,0,0)
            self.picformat  =   picf
            self.picpathok  =   picok
            self.artpathok  =   artok
            self.picindex   =   picidx
            self.artindex   =   artidx
            
            ## Setup Flatten Variables if they have not been set..
            if not self.Emus[self.index].has_key('flatten') :
                self.Emus[self.index]['flatten']    =   {}
                for Key in self.Emus[self.index]['rompath'].keys() :
                    self.Emus[self.index]['flatten'][Key] = 0
            else    :
                if not self.Emus[self.index]['flatten'].has_key(self.Subidx)    :
                    self.Emus[self.index]['flatten'][self.Subidx] = 0

            ## Check Games filehash...
            self.filehash = self.HashFileName(self.index,self.Subidx)
            if os.path.isfile(self.filehash)    :   self.gamesexist = True
            else                                :   self.gamesexist = False
            
            self.DialogP        = xbmcgui.DialogProgress()            
            self.DialogP.create(LANGUAGE[68],LANGUAGE[69])
            
            self.ClearList()    #   Clear all the Info..
            
            tmppath = self.Emus[self.index]['rompath'][self.Subidx]
            if not (self.gamesexist)    :   sortfave,sortnorm = self.GamesFromDir([],[],tmppath,tmppath)
            else                        :   sortfave,sortnorm = self.GamesFromFile([],[])       
            
            self.DialogP.update(90,LANGUAGE[65],LANGUAGE[66],LANGUAGE[67])
            self.DisplayRoms(sortfave)
            self.DisplayRoms(sortnorm)        

            ## Write out records to file..
            if not (self.gamesexist)    : self.PutGames(self.filehash)

            self.controls[20]['control'].setLabel(str(len(self.romListItem))+' '+LANGUAGE[9])
            self.DialogP.close()
        except:
            self.DialogP.close()
            traceback.print_exc()
            Debug(self)


    def ShowFaves(self,Init=False)   :
        try:
            print '--ShowFaves'
            self.setFocus(self.controls[50]['control'])
            if Init == False    :   self.SFX(self.Sounds['select'])
            self.controls[50]['control'].reset()
            self.ViewState  = STATE_FAVES
            self.index      = ''
            self.Subidx     = 0
            
            if bool(int(self.Auto['DUALDISP'])) == True :
                self.CtlButtons(False)
                self.DualDisplay(True)
            else    :
                self.DualDisplay(False)
                self.CtlButtons(True)
            
            self.ButtonLabel(12,'B',True,LANGUAGE[4])
            self.ButtonLabel(14,'X',False,'')
            self.ButtonLabel(16,'Y',False,'')

            self.ClearList()    #   Clear all the Info..
            
            self.gamesexist     = False
            self.RomLabel(LANGUAGE[2])
            
            self.DialogP        = xbmcgui.DialogProgress()
            self.DialogP.create(LANGUAGE[68],LANGUAGE[69])

            EMUS = self.Emus.keys()
            EMUS.sort()
            
            for Emu in EMUS :                                                               # Loop through Emulators
                if self.Emus[Emu].has_key('filehash')   :                                   # Filehash exists - Check for files.
                    for Src in self.Emus[Emu]['name'].keys()    :                           # Loop through sources now.
                        self.filehash = self.HashFileName(Emu,Src)
                        if os.path.isfile(self.filehash)        :                           # Does Hashfile exist.
                            self.index      = Emu
                            self.Subidx     = int(Src)
                            picf,picok,artok,picidx,artidx = self.CheckPics(self.index,self.Subidx,False,False,False,0,0)
                            sortfave,sortnorm = self.GamesFromFile([],[],ForFaves=True)     # Get all Favourites    
                            self.DisplayRoms(sortfave,ForFaves=True,PicData=[picf,picok,artok,picidx,artidx])

            self.controls[20]['control'].setLabel(str(len(self.romListItem))+' '+LANGUAGE[9])
            self.index  = ''
            self.Subidx = 0
            self.DialogP.close()
            if len(self.romListItem) == 0   :
                xbmcgui.Dialog().ok(LANGUAGE[2],LANGUAGE[3])                
                self.ShowEmus()
        except:
            self.DialogP.close()
            traceback.print_exc()
            Debug(self)
        
        
    def DisplayRoms(self,RomArray,ForFaves=False,PicData=[]):
        try:
            print '--DisplayRoms:'
            RomArray.sort()
            for Rom in RomArray :
                if bool(int(self.Auto['SHOWEXT']))  :   RomName =   str(Rom[0]) +'.'+ str(Rom[1])
                else                                :   RomName =   str(Rom[0])
                self.Rom.append(Rom[0])
                self.Ext.append(Rom[1])
                self.Dir.append(Rom[2])
                self.Plays.append(int(Rom[4]))
                if ForFaves == False : 
                    ROMITEM = xbmcgui.ListItem(RomName,Rom[3],iconImage=self.icon_emu)
                else                :
                    ROMITEM = xbmcgui.ListItem(RomName,str('['+ Rom[3] +']'),iconImage=self.icon_emu)
                    self.PicInfo.append([PicData[0],PicData[1],PicData[2],PicData[3],PicData[4]])
                    self.FavesSub.append(int(Rom[5]))
                self.romListItem.append(ROMITEM)
                self.controls[50]['control'].addItem(ROMITEM)
        except:
            self.DialogP.close()
            traceback.print_exc()
            Debug(self)


    def GamesFromDir(self,sortnorm,sortfave,BaseDir,mypath) :
        try:
            print '--GamesFromDir:'
            names = os.listdir(BaseDir)
            if len(BaseDir) == len(mypath)  :   shortdir = ''
            else                            :   shortdir = BaseDir[len(mypath):] +'\\'
            dirs, nondirs = [], []
            TotFiles = len(names) + len(sortnorm) + len(sortfave)
            for name in names:
                if os.path.isdir(os.path.join(BaseDir,name)):   dirs.append(name)
                else                                        :
                    splitrom = string.rsplit(name,'.',maxsplit=1)
                    if len(splitrom) == 2:
                        if splitrom[1].lower() in self.Emus[self.index]['romext'].lower():
                            sortnorm.append([str(splitrom[0]),str(splitrom[1]),str(shortdir),'',0])
                    DonePct = ((len(sortnorm) + len(sortfave))* 100) / TotFiles
                    self.DialogP.update(int(DonePct),LANGUAGE[75] +' ('+ str(name) + ')..')
            print '---Dir :'+ str(shortdir) +' --Dirs:'+ str(len(dirs)) +' --Files:'+ str(len(sortnorm))
            if bool(int(self.Emus[self.index]['flatten'][self.Subidx]))    :
                for name in dirs:
                    path = os.path.join(BaseDir, name)
                    if not os.path.islink(path) :
                        self.GamesFromDir(sortnorm,sortfave,path,mypath)
            return sortfave,sortnorm
        except:
            self.DialogP.close()
            f.close()
            traceback.print_exc()
            Debug(self)


    def GamesFromFile(self,sortnorm,sortfave,ForFaves=False)  :
        try:
            print '--GamesFromFile'
            f=open(self.filehash,"r")
            for line in f:
                splitrom = string.split(line,',')
                if len(splitrom) == 4           :   # Restructure the File..
                    tmprom = string.rsplit(splitrom[0],'.',maxsplit=1)
                    tmpvar = [tmprom[0],tmprom[1],splitrom[2],splitrom[1],0]
                    splitrom = tmpvar
                if      int(splitrom[3]) == 1   :
                    if ForFaves ==  False       :
                        sortfave.append([str(splitrom[0]),str(splitrom[1]),str(splitrom[2]),LANGUAGE[54],int(splitrom[4])])
                    else                        :
                        sortfave.append([str(splitrom[0]),str(splitrom[1]),str(splitrom[2]),self.index,0,self.Subidx])
                else                            :
                    sortnorm.append([str(splitrom[0]),str(splitrom[1]),str(splitrom[2]),'',int(splitrom[4])])
                self.DialogP.update(99,LANGUAGE[75] +' ('+ str(splitrom[0]) + ')..')
            f.close()
            return sortfave,sortnorm
        except:
            self.DialogP.close()
            f.close()
            traceback.print_exc()
            Debug(self)


    def PutGames(self,filehash):
        try:
            print '--PutGames'
            f = open(filehash,"wb")
            for recno in range(len(self.romListItem))  :
                if      self.romListItem[recno].getLabel2() == ''   :   fave = 0
                else                                                :   fave = 1
                f.write(str(self.Rom[recno]) +','+ str(self.Ext[recno]) +','+ \
                        str(self.Dir[recno]) +','+ str(fave) +','+ str(self.Plays[recno]) +',\r\n')
            f.close()
        except:
            traceback.print_exc() 
            Debug(self)
        

    def CheckPics(self,tidx,tsub,picformat,picpathok,artpathok,picindex,artindex):
        try :
            print '--CheckPics'
            if  '%s' in  self.Emus[tidx]['picformat']   :   picformat   =   True
            else                                        :   picformat   =   False
            
            if picformat == True    :
                if self.Emus[tidx]['picpath'][tsub] != ''  :
                    picpathok  =   True
                    picindex   =   tsub
                else    :
                    if tsub  != 0    :
                        if self.Emus[tidx]['picpath'][0] != ''    :
                            picpathok  =   True
                            picindex   =   0
                
                if self.Emus[tidx]['artpath'][tsub] != ''  :
                    artpathok  =   True
                    artindex   =   tsub
                else    :
                    if tsub  != 0    :
                        if self.Emus[tidx]['artpath'][0] != ''    :
                            artpathok  =   True
                            artindex   =   0

            return picformat,picpathok,artpathok,picindex,artindex
        except:
            traceback.print_exc() 
            Debug(self)


    def AddFave(self,recno)    :
        try :
            self.SFX(self.Sounds['faves'])
            if      self.romListItem[recno].getLabel2() == ''   :   self.romListItem[recno].setLabel2(LANGUAGE[54])
            else                                                :   self.romListItem[recno].setLabel2('')  
        except:
            traceback.print_exc() 
            Debug(self)
        

    def LaunchRom(self,rom,emutype):
        try :
            print '--LaunchRom'
            self.SFX(self.Sounds['launch'])
            self.DialogP = xbmcgui.DialogProgress()
            self.DialogP.create(LANGUAGE[5] +'..',LANGUAGE[76])          
            self.Emu_Thread.terminate()
            time.sleep(0.5)
            self.DialogP.update(30,LANGUAGE[76],LANGUAGE[77])    
            if emutype == 'python':
                self.SaveCfg()
                global PYSCRIPT
                PYSCRIPT = self.Emus[self.index]['emupath']
                if bool(int(self.Auto['DOAUTO']))    :   self.AppendReturn(PYSCRIPT)
                self.DialogP.close()    
                self.close()
            else    :
                if bool(int(self.Auto['DOAUTO']))    :   self.Autoexec('WRITE')
                self.SaveCfg()
                self.DialogP.update(60,LANGUAGE[77],LANGUAGE[78])    
                SHORTCUT = HOME_DIR + CUT_FILE
                f=open(SHORTCUT, "wb")
                f.write("<shortcut>\n")
                f.write("    <path>" + self.Emus[self.index]['emupath'] + "</path>\n")
                if emutype == 'emugame':
                    f.write("    <custom>\n")
                    f.write("       <game>" + self.Emus[self.index]['rompath'][self.Subidx] + rom + "</game>\n")
                    f.write("    </custom>\n")
                f.write("</shortcut>\n")
                f.close()
                self.DialogP.update(99,LANGUAGE[78],LANGUAGE[5] +'...')    
                xbmc.executebuiltin('XBMC.Runxbe(' + SHORTCUT + ')')
                self.DialogP.close()    
        except:
            self.DialogP.close()    
            traceback.print_exc() 
            Debug(self)


    def SysCfg(self)    :
        try :
            self.SFX(self.Sounds['dialog'])
            CfgList =   []
            if bool(int(self.Auto['DOAUTO']))   :   CfgList.append(LANGUAGE[56] +' '+ LANGUAGE[58])
            else                                :   CfgList.append(LANGUAGE[56] +' '+ LANGUAGE[57])
            if bool(int(self.Auto['DUALDISP'])) :   CfgList.append(LANGUAGE[55] +' '+ LANGUAGE[58])
            else                                :   CfgList.append(LANGUAGE[55] +' '+ LANGUAGE[57])
            if bool(int(self.Auto['SHOWEXT']))  :   CfgList.append(LANGUAGE[8]  +' '+ LANGUAGE[58])
            else                                :   CfgList.append(LANGUAGE[8]  +' '+ LANGUAGE[57])
            CfgList.append(LANGUAGE[10] +' ['+ str(self.Auto['SOUND']) +']')    
            CfgList.append(LANGUAGE[28])
            choice = xbmcgui.Dialog().select(LANGUAGE[60],CfgList)
            if      choice == 0                 :   self.Auto['DOAUTO']     =   self.ToggleVar(self.Auto['DOAUTO'])
            elif    choice == 1                 :   self.Auto['DUALDISP']   =   self.ToggleVar(self.Auto['DUALDISP'])
            elif    choice == 2                 :   self.Auto['SHOWEXT']    =   self.ToggleVar(self.Auto['SHOWEXT'])
            elif    choice == 3                 :
                dirlist =   []
                for dirs in os.listdir(SOUND)   :
                    if os.path.isdir(SOUND + dirs)  :   dirlist.append(dirs)
                dirlist.sort()
                dirlist.append('OFF')
                current =   dirlist.index(self.Auto['SOUND'])
                if current  ==  len(dirlist) - 1    :   self.Auto['SOUND']  =   str(dirlist[0])
                else                                :   self.Auto['SOUND']  =   str(dirlist[current + 1])
                self.SetSounds(self.Auto['SOUND'])
            else                :   return
            self.SysCfg()
        except:
            traceback.print_exc() 
            Debug(self)


    def ToggleVar(self,Var) :
        if bool(int(Var))   :   return 0
        else                :   return 1
        
        
    def onControl(self, control):
        if      control == self.controls[4]['control'] or control == self.controls[5]['control'] or \
                control == self.controls[6]['control'] or control == self.controls[7]['control']  :
            self.NavButtons(False)
            if      control == self.controls[4]['control']         :
                self.ModEmu()
            elif    control == self.controls[5]['control']         :
                self.AddEmu()        
            elif    control == self.controls[6]['control']         :
                self.DelEmu()
            elif    control == self.controls[7]['control']         :
                self.SysCfg()
            else                                                   :
                pass
            self.NavButtons(True)            
        elif    control == self.controls[50]['control']        :
            tlab    =   self.controls[50]['control'].getSelectedItem().getLabel()
            tlab2   =   self.controls[50]['control'].getSelectedItem().getLabel2()
            tnum    =   self.controls[50]['control'].getSelectedPosition()
            if      self.ViewState == STATE_EMU             :
                if self.Emus[tlab]['type'] == 'emugame' :
                    self.ShowRoms(tlab)
                else                                    :
                    self.index = tlab
                    self.LaunchRom('null',self.Emus[tlab]['type'])
            elif    self.ViewState == STATE_ROMS    :
                self.Plays[tnum] = self.Plays[tnum] + 1
                self.LaunchRom(self.Dir[tnum] + self.Rom[tnum] +'.'+ \
                               self.Ext[tnum],self.Emus[self.index]['type'])
            elif    self.ViewState == STATE_FAVES    :
                self.index  = tlab2[1:-1]
                self.Subidx = int(self.FavesSub[tnum])
                self.LaunchRom(self.Dir[tnum] + self.Rom[tnum] +'.'+ \
                               self.Ext[tnum],self.Emus[self.index]['type'])
            else                                    :   pass
        else                                        :   pass



    def onAction(self,action):
        if      action == ACTION_MOVE_LEFT  or action == ACTION_MOVE_RIGHT or action == ACTION_MOVE_UP \
            or  action == ACTION_MOVE_UP    or action == ACTION_MOVE_DOWN  or action == ACTION_PAGE_UP \
            or  action == ACTION_PAGE_DOWN  or action == ACTION_NEXT_ITEM  or action == ACTION_PREV_ITEM    :
            self.SFX(self.Sounds['move'])
        if      action == ACTION_PREVIOUS_MENU      :   self.CloseDown()    
        elif    action == ACTION_B                  :
            if self.index != '' and self.ViewState == STATE_ROMS    :
                self.PutGames(self.filehash)
                self.ShowEmus()
            elif self.ViewState == STATE_FAVES      :   self.ShowEmus()
            elif self.ViewState == STATE_EMU        :   self.CloseDown()
            else                                    :   pass
        elif    action == ACTION_X                  :
            if  self.ViewState == STATE_ROMS and self.getFocus() == self.controls[50]['control']   :
                self.AddFave(self.controls[50]['control'].getSelectedPosition())
            elif self.ViewState == STATE_EMU        :   self.ShowFaves()
            else                                    :   pass
        elif    action == ACTION_Y                  :
            if  self.ViewState == STATE_ROMS and self.getFocus() == self.controls[50]['control']   :
                self.NavButtons(False)
                self.Sources()
                self.NavButtons(True)
            else                                    :   pass
        else                                        :   pass


    def CloseDown(self) :
        self.SFX(self.Sounds['end'])
        self.Emu_Thread.terminate()
        self.SaveCfg()
        self.close()


    def Sources(self)   :
        try:
            self.SFX(self.Sounds['dialog'])
            SrcList =   []
            SrcFunc =   []
            if self.Emus[self.index].has_key('view')    :   tview = int(self.Emus[self.index]['view'])
            else                                        :   tview = 0
            SrcList.append(LANGUAGE[48] +' ('+ str(tview) +')')
            SrcFunc.append(['DEFAULT',self.Subidx])
            for Key,Val in self.Emus[self.index]['name'].iteritems() :
                if Key != self.Subidx   :
                    SrcList.append(LANGUAGE[50] +': ('+   str(Val)  +':'+ str(Key) +')')
                    SrcFunc.append(['SWITCH',Key,Val])
            SrcList.append(LANGUAGE[51] +': ('+   \
                           str(self.Emus[self.index]['name'][self.Subidx])  +':'+ \
                           str(self.Subidx) +')')
            SrcFunc.append(['MODIFY',self.Subidx,self.Emus[self.index]['name'][self.Subidx]])
            if self.Subidx != 0 :
                SrcList.append(LANGUAGE[52] +': ('+   \
                               str(self.Emus[self.index]['name'][self.Subidx])  +':'+ \
                               str(self.Subidx) +')')
                SrcFunc.append(['DELETE',self.Subidx,self.Emus[self.index]['name'][self.Subidx]])
            SrcList.append(LANGUAGE[49])
            SrcFunc.append(['ADDSRC'])            
            if self.Emus[self.index].has_key('filehash') and os.path.isfile(self.filehash)  :
                SrcList.append(LANGUAGE[61])
                SrcFunc.append(['CLEARCACHE',self.filehash])                            
            SrcList.append(LANGUAGE[28] +'..')
            SrcFunc.append(['CANCEL',-1])
            result  = xbmcgui.Dialog().select(LANGUAGE[53],SrcList)
            if      result == -1 or SrcFunc[result][0] == 'CANCEL' :   return
            self.SrcChange(SrcFunc[result])
            return
        except:
            traceback.print_exc()
            Debug(self)


    def SrcChange(self,SrcFunc):
        try :
            if      SrcFunc[0] == 'ADDSRC'  :
                FreeSlot    =  False
                SlotNo      =   0
                while FreeSlot == False     :
                    if not self.Emus[self.index]['name'].has_key(SlotNo)    :   FreeSlot    =   True
                    else                                                    :   SlotNo      +=  1
                self.AddModSource(SlotNo)
                answer = xbmcgui.Dialog().yesno(LANGUAGE[50] +'..',LANGUAGE[79],LANGUAGE[80])
                if (answer) :   self.ShowRoms(self.index,Source=SlotNo)
                                    
            elif    SrcFunc[0] == 'MODIFY'      :
                self.AddModSource(SrcFunc[1])
                
            elif    SrcFunc[0] == 'DELETE'      :
                answer = xbmcgui.Dialog().yesno(LANGUAGE[52] +'..',LANGUAGE[81],str(SrcFunc[1]) +': '+ str(SrcFunc[2]))
                if (answer) :
                    self.ClearCache(self.index,SrcFunc[1])
                    for k in ['name','rompath','picpath','artpath'] :
                        del self.Emus[self.index][k][SrcFunc[1]]
                    if self.Emus[self.index].has_key('view') :
                        if int(self.Emus[self.index]['view']) == self.Subidx :
                            self.Emus[self.index]['view'] = 0
                    else    :
                        self.Emus[self.index]['view'] = 0
                    self.ShowRoms(self.index,Source=int(self.Emus[self.index]['view']))
                    
            elif    SrcFunc[0] == 'SWITCH'      :   self.ShowRoms(self.index,Source=SrcFunc[1])            
            elif    SrcFunc[0] == 'DEFAULT'     :   self.Emus[self.index]['view'] =   SrcFunc[1]            
            elif    SrcFunc[0] == 'CLEARCACHE'  :
                answer = xbmcgui.Dialog().yesno(LANGUAGE[82],LANGUAGE[83],LANGUAGE[84])
                if (answer) :
                    FaveRom = []
                    for Rom in self.romListItem :
                        if Rom.getLabel2()  !=  ''  :   FaveRom.append(Rom.getLabel())
                    os.remove(self.filehash)
                    self.ShowRoms(self.index,Source=self.Subidx,Faves=FaveRom)
            else                                :   return
        except:
            traceback.print_exc()
            Debug(self)


    def AddModSource(self,No)  :
        try :
            modarr          =   deepcopy(self.Emus[self.index])
            modarr['title'] =   self.index
            Status,modarr   =   self.ConfMenu(modarr,Indx=No)                
            if Status   == True  :
                ClearIt = False
                if self.Emus[self.index]['rompath'].has_key(No)    :
                    if modarr['rompath'][No] != self.Emus[self.index]['rompath'][No]   :   ClearIt = True
                    if not self.Emus[self.index].has_key('flatten')     : self.Emus[self.index]['flatten'] = {}
                    if not self.Emus[self.index]['flatten'].has_key(No) : self.Emus[self.index]['flatten'][No] = 0
                    if modarr['flatten'][No] != self.Emus[self.index]['flatten'][No]   :   ClearIt = True
                NewTitle                =   modarr.pop('title')
                del self.Emus[NewTitle]
                self.Emus[NewTitle]     =   {}
                self.Emus[NewTitle].update(modarr)
                if ClearIt  :
                    self.ClearCache(NewTitle,No)
                    self.ShowRoms(self.index,Source=No)
        except:
            traceback.print_exc()
            Debug(self)


    def ClearCache(self,EmuName,EmuNo) :
        try :
            FileHash = self.HashFileName(EmuName,EmuNo)
            if os.path.isfile(FileHash) :   os.remove(FileHash)        
        except:
            traceback.print_exc()
            Debug(self)


    def HashFileName(self,EmuName,EmuNo) :
        try :
            if not self.Emus[EmuName].has_key('filehash'):
                self.Emus[EmuName]['filehash']   =   hash(str(self.Emus[EmuName]))
            return GAMEDIR +'EMU'+ str(EmuNo) +'_'+ str(self.Emus[EmuName]['filehash']) + '.csv'
        except:
            traceback.print_exc()
            Debug(self)
              

class EmuThread(threading.Thread):
    def __init__(self,overlay):
        threading.Thread.__init__(self)
        self.running    = True
        self.gui        = overlay
        
    def terminate(self):
        self.running = False
        self.join(1)

    def run(self):
        self.last_recno     =   -1
        self.last_recnm     =   ''
        self.last_recnm2    =   ''
        while (self.running):
            try:
                wdFocus = self.gui.getFocus() 
                if self.gui.controls[50]['control'] == wdFocus: 
                    self.recnm   =   self.gui.controls[50]['control'].getSelectedItem().getLabel()
                    self.recnm2  =   self.gui.controls[50]['control'].getSelectedItem().getLabel2()
                    self.recno   =   self.gui.controls[50]['control'].getSelectedPosition()  
                    if self.recno != self.last_recno or self.recnm != self.last_recnm    :
                        self.last_recno     =   self.recno
                        self.last_recnm     =   self.recnm

                        if      self.gui.ViewState == STATE_EMU     :
                            self.gui.controls[21]['control'].setImage(self.gui.Emus[self.recnm]['icon'])
                                
                        elif    self.gui.ViewState == STATE_ROMS   :
                            self.MySlides   = []
                            picpathok       = self.gui.picpathok
                            artpathok       = self.gui.artpathok
                            picindex        = self.gui.picindex
                            artindex        = self.gui.artindex
                            tidx            = self.gui.index                            
                            self.ShowEm(picpathok,artpathok,picindex,artindex,tidx,STATE_ROMS)
                            
                        elif    self.gui.ViewState == STATE_FAVES   :
                            self.MySlides   = []
                            picpathok       = self.gui.PicInfo[self.recno][1]
                            artpathok       = self.gui.PicInfo[self.recno][2]
                            picindex        = self.gui.PicInfo[self.recno][3]
                            artindex        = self.gui.PicInfo[self.recno][4]                            
                            tidx            = self.recnm2[1:-1]                            
                            self.ShowEm(picpathok,artpathok,picindex,artindex,tidx,STATE_FAVES)
                               
                        else    :   pass
                else    :
                    self.last_recno     =   -1
                    self.last_recnm     =   ''
                    self.last_recm2     =   ''
                    self.gui.controls[21]['control'].setImage(HOME_DIR + 'default.tbn')
            except:
                #traceback.print_exc()
                pass
            time.sleep(0.75)

            
    def QueuePics(self,pathtofile) :
        try :
            if  os.path.exists(pathtofile)  :
                if      os.path.isfile(pathtofile)      :   self.MySlides.append(pathtofile)
                else                                    :
                    for Img in os.listdir(pathtofile)   :   self.MySlides.append(pathtofile +'\\'+ Img)
        except:
            #traceback.print_exc()
            pass


    def ShowEm(self,picpathok,artpathok,picindex,artindex,tidx,MyView) :
        try :
            if bool(int(self.gui.Auto['DUALDISP'])) :
                self.gui.controls[96]['control'].setImage(self.gui.Emus[tidx]['icon'])
            else                                    :
                self.MySlides.append(self.gui.Emus[tidx]['icon'])

            rom = self.gui.Rom[self.recno]
            if (picpathok)  :   self.QueuePics(self.gui.Emus[tidx]['picpath'][picindex] + \
                                               self.gui.Emus[tidx]['picformat'] % rom)
            if (artpathok)  :   self.QueuePics(self.gui.Emus[tidx]['artpath'][artindex] + \
                                               self.gui.Emus[tidx]['picformat'] % rom)
            if len(self.MySlides) > 1   :
                myslides    =   len(self.MySlides) - 1
                start       =   0
                while (self.running) and \
                      self.recno            == self.gui.controls[50]['control'].getSelectedPosition() and \
                      self.gui.ViewState    == MyView:
                    self.gui.controls[21]['control'].setImage(self.MySlides[start])
                    if start < myslides :   start += 1
                    else                :   start =  0
                    time.sleep(0.75)
            elif len(self.MySlides) == 1:
                self.gui.controls[21]['control'].setImage(self.MySlides[0])
                time.sleep(0.75)
            else                        :
                self.gui.controls[21]['control'].setImage(HOME_DIR + 'default.tbn')
                time.sleep(0.75)
        except:
            #traceback.print_exc()
            pass

        
EmuGui  =   Launcher()
OkCount =   0
if LANGOK                   :   OkCount += 1
else                        :   xbmcgui.Dialog().ok("LANGUAGE ERROR","Problem loading language file..")
if CORE                     :   OkCount += 1
else                        :   xbmcgui.Dialog().ok("MODULE ERROR","Problem loading core module..")
if EmuGui.SUCCEEDED         :   OkCount += 1
else                        :   xbmcgui.Dialog().ok("GUI ERROR","Problem loading gui system..")

if OkCount == 3             :
    EmuGui.doModal()
    del EmuGui

xbmc.executescript(PYSCRIPT)
