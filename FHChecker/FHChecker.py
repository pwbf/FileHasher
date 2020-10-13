import os
import re
import xml.etree.ElementTree as ET
from hashlib import md5, sha256

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
ALGOR = 'SHA256'

def filehasherMD5(fname):
    return (md5(open(fname,'rb').read()).hexdigest()).upper()

def filehasher(fname):
    return (sha256(open(fname,'rb').read()).hexdigest()).upper()

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

print(">>> Start Checking")

MATC_FLIST = []
NMAT_FLIST = []
MISS_FLIST = []

Total_FLIST = []

for file in root.findall('FILE'):
    FNAME = file.get('FILENAME')
    ALGOR = file.find('ALGORITHM').text
    FHASH = file.find('HASH').text

    Total_FLIST.append(FNAME)
    print("Now checking >> "+FNAME, end="\r")

    if FNAME in FILES:
        FCHECK = filehasher(FNAME)
    
        if(FCHECK == FHASH):
            MATC_FLIST.append(FNAME)
        else:
            NMAT_FLIST.append(FNAME)
    else:
        MISS_FLIST.append(FNAME)

print("                                                                                                        ", end="\r")
print("\n################Checking Finished#################")
print("Evaulation report:")

print("Checked file\n"
      +"Total: "+str(len(Total_FLIST))+"\n"
      +"Succeed: "+str(len(MATC_FLIST))+"\n"
      +"Corrupted: "+str(len(NMAT_FLIST))+"\n"
      +"Missing: "+str(len(MISS_FLIST))+"\n")

print("##################################################")

print("Checked files:")
for index, fn in enumerate(Total_FLIST):
    print("["+str(index)+"] ",fn)
print()

print("##################################################")
print("[V]Matched files:")
for index, fn in enumerate(MATC_FLIST):
    print("["+str(index)+"] ",fn)
print()

print("##################################################")
print("[X]Corrupted files:")
for index, fn in enumerate(NMAT_FLIST):
    print("["+str(index)+"] ",fn)
print()

print("##################################################")
print("[#]Missing files:")
for index, fn in enumerate(MISS_FLIST):
    print("["+str(index)+"] ",fn)
print()

print("##################################################")
os.system("pause")