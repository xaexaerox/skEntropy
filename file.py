###############################################################
#
#
#
# This program will take a file as input and produce its type in ouput
#
#
#Mavenkp
#
#Jan 2016
#
#
#

import os
import sys
import codecs
import binascii
import base64

def file(file):
    filetype= ""
    if os.path.isfile(file):
        fileopen = open(file,"rb")
        fileread =fileopen.read()
        exemagic = fileread[0:2].decode("UTF-8")
        print(exemagic)
        
        lfname = fileread[60]
        print(hex(lfname))
        
        peheader = fileread[lfname:lfname+4].decode("UTF-")
        print(peheader)
        
        machinenumb = lfname+4
        machine = fileread[machinenumb:machinenumb+4]
        print( base64.b16decode(machine))
        ordermachine = chr(machine[3])+chr(machine[2])+chr(machine[1])+chr(machine[0])

        #print(binascii.hexlify(ordermachine))
        print(ordermachine)
        print(machine)
               

    else:
        filetype= "File doesn't exist"

    return filetype

file("C:\\Windows\\SysWOW64\\attrib.exe")
file("C:\\Windows\\hh.exe")

EXE_MAGIC = "MZ"
PE_MAGIC = "PE"
