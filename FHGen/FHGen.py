
import os
from hashlib import md5, sha256
from xml.etree import ElementTree
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, Comment


BUF_SIZE = 65535
PATH = "./"
FILES = os.listdir(PATH)
THISPATH = os.getcwd()
THISDIR = os.path.basename(THISPATH)
XMLNAME = "_HashChecker.xml"
XMLHASH = ""
ORIGIN_FULLPATH = THISPATH+"\\"+XMLNAME
NEW_FULLPATH = THISPATH+"\\"

FNAME = ''
FUID = ''
FHASH = ''
ALGOR = 'SHA256'

ROOT = Element('FILES')

def filehasher(fname):
    return (sha256(open(fname,'rb').read()).hexdigest()).upper()

def filehasherMD5(fname):
    return (md5(open(fname,'rb').read()).hexdigest()).upper()

def prettify(elem):
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

for f in FILES:
    fullpath = os.path.join(PATH, f)
    if os.path.isfile(fullpath) and f != XMLNAME:
        FNAME = f
        print("Hashing >> Filename:", FNAME)
        FHASH = filehasher(fullpath)

        CHILD = SubElement(ROOT, 'FILE', {'FILENAME': FNAME})
        E_ALGRO = SubElement(CHILD, 'ALGORITHM')
        E_ALGRO.text = ALGOR
        E_FHASH = SubElement(CHILD, 'HASH')
        E_FHASH.text = FHASH


        print(ALGOR,':', FHASH,'\n')

with open(XMLNAME, "w", encoding = "utf-8") as GENFILE:
    print('Writing to XML file...')
    GENFILE.write(prettify(ROOT))

XMLHASH = "_FHasher_"+filehasherMD5(XMLNAME)+".xml"
NEW_FULLPATH += XMLHASH
print('File Hashing result: ', XMLHASH)
os.rename(ORIGIN_FULLPATH,NEW_FULLPATH)
os.system("pause")
