import hashlib
import os
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
ALGOR = 'SHA3-256'

ROOT = Element('FILES')

def filehasher(fname):
    return (hashlib.sha3_256(open(fname,'rb').read()).hexdigest()).upper()

def filehasherMD5(fname):
    return (hashlib.md5(open(fname,'rb').read()).hexdigest()).upper()

def prettify(elem):
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

for f in FILES:
    fullpath = os.path.join(PATH, f)
    if os.path.isfile(fullpath) and f != XMLNAME:
        FNAME = f
        print("File:", FNAME)
        FHASH = filehasher(fullpath)

        CHILD = SubElement(ROOT, 'FILE', {'FILENAME': FNAME})
        E_ALGRO = SubElement(CHILD, 'ALGORITHM')
        E_ALGRO.text = ALGOR
        E_FHASH = SubElement(CHILD, 'HASH')
        E_FHASH.text = FHASH


        print(ALGOR,':', FHASH)

with open(XMLNAME, "w", encoding = "utf-8") as GENFILE:
    GENFILE.write(prettify(ROOT))

XMLHASH = filehasherMD5(XMLNAME)
NEW_FULLPATH += "_FHasher_"+XMLHASH+".xml"
os.rename(ORIGIN_FULLPATH,NEW_FULLPATH)
os.system("pause")
