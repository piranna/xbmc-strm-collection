import  os  ,   traceback   ,   string  ,   struct, operator
from    xml.dom     import minidom
from    types       import *

def GetATag(Elements,ForXml):
    try :
        Xml         =   {}
        xmldoc      =   minidom.parse(ForXml)
        ForTag      =   xmldoc.getElementsByTagName(Elements)
        TagName     =   ForTag[0].nodeName
        TagValue    =   ForTag[0].childNodes[0].data
        xmldoc.unlink()
        return TagValue
    except  :
        traceback.print_exc() 
        return ''


def GetAllTags(Elements,ForXml,Root='title',Type='default'):
    try:
        Xml =   {}
        xmldoc = minidom.parse(ForXml)
        ForTag = xmldoc.getElementsByTagName(Elements)
        for Elements in ForTag:
            XML     =   []   ;   TagName     = ''    ;   TagValue    = ''   ; root_name = ''  
            for Tag in Elements.childNodes          :
                if Tag.nodeType == Tag.ELEMENT_NODE :
                    TagAtts     = -1
                    TagName     = Tag.nodeName  
                    if len(Tag.attributes) >  0     :   TagAtts     = int(Tag.attributes["id"].value)   
                    if len(Tag.childNodes) != 0     :   TagValue    = Tag.childNodes[0].data
                    else                            :   TagValue    = ''
                    if TagAtts  != -1               :   XML.append([TagName,TagValue,TagAtts])
                    else                            :
                        if TagName == Root          :   root_name   = TagValue
                        else                        :   XML.append([TagName,TagValue])
            if not Xml.has_key(root_name)           :   Xml[root_name]  =   {}
            for items in XML        :
                if len(items) == 2  :
                    if Type == 'default'    :   Xml[root_name][items[0]]    =   items[1]
                    else                    :
                        if not Xml[root_name].has_key(items[0]) :
                            Xml[root_name][items[0]]    =   []
                        Xml[root_name][items[0]].append(items[1])
                else                :
                    if not Xml[root_name].has_key(items[0])  :
                        Xml[root_name][items[0]]  =   {}
                    Xml[root_name][items[0]][items[2]]  =   items[1]
                
        xmldoc.unlink()
        return Xml
    except:
        traceback.print_exc() 
        return {}
    

def Check_Lang(LANGDIR,GUIXML):
    try:
        LANGOK          =   False   
        LANGUAGE        =   {}
        lang_exp        =   GetATag('language',GUIXML)
        if lang_exp     !=  ''  :   XBMC_LANGUAGE   =   lang_exp.lower()            
        else                    :   XBMC_LANGUAGE   =   'english'           
        print '-- lang_exp:'+ str(lang_exp)
        
        if os.path.isfile(LANGDIR + str(XBMC_LANGUAGE) + '.xml')            :      
            XBMC_LANGDIR        =   LANGDIR + str(XBMC_LANGUAGE) +'.xml'
            LANGOK              =   True
        else                                                                :   
            if os.path.isfile(LANGDIR + 'english.xml')                      :  
                XBMC_LANGDIR    =   LANGDIR + 'english.xml'
                XBMC_LANGUAGE   =   'english'
                LANGOK          =   True       
        print '-- LANGOK:'+ str(LANGOK) +'\n-- XBMC_LANGDIR:'+ str(XBMC_LANGDIR)

        if  LANGOK  == True     :                                               
            LANGOK  == False                                                    
            Lang                =   GetAllTags('language',XBMC_LANGDIR)
            
            if Lang.has_key(XBMC_LANGUAGE)                                  :   
                if Lang[XBMC_LANGUAGE].has_key('string')                    :  
                    if len(Lang[XBMC_LANGUAGE]['string'])   >   40          :   
                        LANGOK      =   True                                   
                        LANGUAGE    =   Lang[XBMC_LANGUAGE]['string']

        return LANGOK,LANGUAGE
    except:
        traceback.print_exc() 
        return False,{}


def PutConfig(ForTag,ForXml):
    try:
        print '--PutConfig'
        f = open(ForXml,"wb")
        f.write('<config>\n')
        for Section in ForTag.keys()   :
            for MainTag in ForTag[Section].keys():
                f.write('<'+ Section +'>\n')
                f.write('\t<title>'+ MainTag + '</title>\n')
                for SubTag in ForTag[Section][MainTag].keys():
                    if type(ForTag[Section][MainTag][SubTag]) is DictType   :
                        for Ids in ForTag[Section][MainTag][SubTag].keys()  :
                            f.write('\t<'+ SubTag +' id=\"'+ str(Ids) +'\">'+ str(ForTag[Section][MainTag][SubTag][Ids]) +'</'+ SubTag +'>\n')
                    else                            :
                        f.write('\t<'+ SubTag +'>'+ str(ForTag[Section][MainTag][SubTag]) +'</'+ SubTag +'>\n')
                f.write('</'+ Section +'>\n')
        f.write('</config>\n')
        f.close()
    except:
        traceback.print_exc() 


def XbeInfo(FileName):
    try :
        XbeDta          =   {}
        if os.path.isfile(FileName) and FileName.endswith('.xbe')   :
            xbe         =   open(FileName,'rb')
            ## Get XbeId Data ##
            xbe.seek(0x104)
            tLoadAddr   =   xbe.read(4)
            xbe.seek(0x118)
            tCertLoc    =   xbe.read(4)
            LoadAddr    =   struct.unpack('L',tLoadAddr)
            CertLoc     =   struct.unpack('L',tCertLoc)
            CertBase    =   CertLoc[0] - LoadAddr[0]
            CertBase    +=  8
            IdStart     =   xbe.seek(CertBase)
            tIdData     =   xbe.read(4)
            IdData      =   struct.unpack('L',tIdData)
            ## Get Xbe Title ##
            XbeTitle    =   ''
            for dta in struct.unpack(operator.repeat('H',40),xbe.read(0x0050)):
                try     :
                    if dta != 00  :   XbeTitle += str(unichr(dta))
                except  :   pass
            XbeDta['Title']     =   str(XbeTitle)
            XbeDta['Id']        =   str(hex(IdData[0])[2:-1]).lower().rjust(8,'0')
            XbeDta['Path']      =   str(FileName)
            xbe.close()
        return XbeDta
    except  :
        xbe.close()
        return {}

