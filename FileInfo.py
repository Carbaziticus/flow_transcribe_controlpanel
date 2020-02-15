#!python3

# FileInfo.py

import os
import sys

'''
 Construct the paths of the ConfigParser files (config, defaults and license)
 based on the current directory (the dir from which the calling program is run)
 and the login user home directory.
'''


def appDir():
    # appdirectory = os.path.dirname(os.path.abspath(__file__))
    appdirectory = os.path.dirname(sys.argv[0])
    return(appdirectory)


def currentDir():  # location from which this program is running
    if getattr(sys, 'frozen', False):
        # we are running in a bundle
        currentdirectory = sys._MEIPASS  # the bundle directory
    else:
        # we are running in a normal Python environment
        currentdirectory = os.path.dirname(os.path.abspath(__file__))
    # currentdirectory = os.path.dirname(os.path.abspath(__file__))
    return(currentdirectory)


def defaultsPath():  # include this default cfg in the app bundle or script directory
    defaultsfilepath = os.path.join(currentDir(), 'defaults.cfg')
    # defaultsfilepath = os.path.join(currentDir(), "catdv_backup_defaults.cfg")
    return(defaultsfilepath)


def configPath():  # should be user home dir '.appname.cfg'
    configfilepath = os.path.join(os.path.expanduser('~'), '.Transcribe.cfg')
    # configfilepath = os.path.join(currentDir(), 'catdv_backup.cfg')
    return(configfilepath)


def licensePath():  # should be user home dir '.appname.lic'
    licensefilepath = os.path.join(os.path.expanduser('~'), '.Transcribe.lic')
    # if not os.path.exists(licensefilepath):
    #     licensefilepath = ''
    #     print('licensefilepath:', licensefilepath)
    return(licensefilepath)
