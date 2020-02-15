#! python3

# CPio.py

import os

import configparser as cp


def readCP(file):  # filepath is either configfile, defaultsfile or licensefile.
    # does not attempt to interpret special chars when parsing a cp file.
    # prefer ':' as the key:value delimiter, but '=' is understood as well
    cp_obj = cp.ConfigParser(interpolation=None, delimiters=(':', '='))  # create the cp object
    if not os.path.exists(file):
        return(cp_obj)  # file does not esist.  Return the empty cp obkect
    try:
        cp_obj.read_file(open(file))  # load the cp object with values from file
        return(cp_obj)
    except cp.Error as err:
        return(err)  # the file contents may not be formatted correctly


def writeCP(cp_obj, file):
    #  the try block catches errors with open(file, 'w')
    try:
        with open(file, 'w') as outfile:
            cp_obj.write(outfile)
            # outfile.write('Hello World')
    except IOError:
        print('CP cannot write to:', file)

    # cp_obj.write(open(file, 'w'))
