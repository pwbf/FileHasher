import hashlib
import os
import xml.etree.ElementTree as ET


BUF_SIZE = 65535
PATH = "./"
FILES = os.listdir(PATH)
THISDIR = os.path.basename(os.getcwd())
XMLNAME = "_" + THISDIR + ".xml"

root = None
try:
    root = ET.parse(XMLNAME).getroot()
except:
    while root is None:
        try:
            root = ET.parse(input("Could not find XML document, enter filename manually? ")).getroot()
        except:
            pass

FNAME = ''
FUID = ''
FHASH = ''
ALGOR = 'SHA3-256'


def filehasher(fname):
    return (hashlib.sha3_256(open(fname,'rb').read()).hexdigest()).upper()

for file in root.findall('FILE'):
    FNAME = file.get('FILENAME')
    ALGOR = file.find('ALGORITHM').text
    FHASH = file.find('HASH').text
    
    if FNAME in FILES:
        FCHECK = filehasher(FNAME)
    
        if(FCHECK == FHASH):
            print("[V] ",FNAME, end="")
            print(" >> File hashing("+ALGOR+") Matched")
        else:
            print("[X] ",FNAME, end="")
            print()
            print('Registered:'+ FHASH)
            print('Calculated:'+ FCHECK)
            print(" >> File hashing("+ALGOR+") Not Matching")
    else:
        print("[#] ",FNAME, end="")
        print(" >> File NOT FOUND!!")
    print()

os.system("pause")