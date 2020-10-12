import hashlib
import os
import re
import xml.etree.ElementTree as ET


BUF_SIZE = 65535
PATH = "./"
FILES = os.listdir(PATH)

reFNAME = r"\_FHasher\_(([0-9]|[A-F]){32})\.xml"
reMD5 = r"([0-9]|[A-F]){32}"
reFLIST = []
reELIST = []
reHLIST = []
CORRECT = ''

root = None

FNAME = ''
FUID = ''
FHASH = ''
ALGOR = 'SHA3-256'

def filehasherMD5(fname):
    return (hashlib.md5(open(fname,'rb').read()).hexdigest()).upper()

def filehasher(fname):
    return (hashlib.sha3_256(open(fname,'rb').read()).hexdigest()).upper()

for fn in FILES:
    if(re.search(reFNAME, fn)):
        reFLIST.append(fn)
        reELIST.append((fn.split('_')[2]).split('.')[0])
        reHLIST.append(filehasherMD5(fn))

for index, fh in enumerate(reHLIST):
    if(fh == reELIST[index]):
        CORRECT = reFLIST[index]
        break
        print("Using "+CORRECT+" as record")

try:
    root = ET.parse(CORRECT).getroot()
except:
    while root is None:
        try:
            mfile = input("Could not find XML document, enter filename manually? ")
            mhash = (input("Insert XML md5 for checking?(N for NO or md5) ")).upper()
            if(mhash != 'N'):
                if(re.search(reMD5, mhash)):
                    hash = filehasherMD5(mfile)
                    if(hash == mhash):
                        print("XML file's hashing is correct")
                        root = ET.parse(mfile).getroot()
                    else:
                        print("Error, hash value isn't matching, maybe the wrong file or corrupted file?")
            else:
                print("Okay! we are not going to check XML file is correct")
                root = ET.parse(mfile).getroot()

        except:
            pass
        print()

print("##################################################")
print("#################Start evaluating#################")


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
    
print("###############Evaluation Finished################")
print("##################################################")
os.system("pause")