import os
HOME_DIR    =   os.getcwd().replace(";","")+"\\"
RETURN      =   False
if os.path.isfile(HOME_DIR +'emuflag.chk')  :   ## Return Active
    os.remove(HOME_DIR +'emuflag.chk')
    RETURN = True
if (RETURN) :
    import xbmc
    xbmc.executescript(HOME_DIR + 'default.py')
