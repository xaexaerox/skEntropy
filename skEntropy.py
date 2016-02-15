######################################################################################################################
#
#   The main purpose of this tool is to detect packed excutables using entropy difference method 
#
#   Author : Mavenkp
#   Date   : Dec 2015
#   Email  : kamlapati[at]gmail.com
#
#
#
#
##################################################################################################################



import math
import sys
import getopt
import os
#import pycrypto 
import pefile
import AES
import binascii
import KNN


def HsetReduction(data):
    """ Entropy calculation using set-reduction method"""
    if not data:
        return 0
    entropy=0
    proba_x=[]
    for x in range(256):
        proba_x.append(float(data.count(((x)))/len(data)))
        #print("proba_x",proba_x)
    proba_x=sorted(proba_x, key=float, reverse=True) 
    for x in range(100):
        if ( proba_x[x] >0 and proba_x[x] < 1):
            entropy += -proba_x[x]*math.log(proba_x[x],2)
    return entropy

def H(data):
    """Calculate entropy of complete file """
    if not data:
        return 0
    entropy=0
    #print(data)
    for x in range(256):
        #print(data,"\n",data.count(((x))))
        proba_x =float(data.count(((x)))/len(data))
        if proba_x >0 :
            entropy += -proba_x*math.log(proba_x,2)
    return entropy

def entropy_scan(data, block_size):
    #print(data)
    count=0
    entropyData=0
    for block in( data[x:block_size+x] for x in range (0,len(data),block_size)):
        entropyBlock = H(block)
        if(entropyBlock>7.199):
            return 1
        if(int(entropyBlock) != 0):
            entropyData=entropyData+entropyBlock
            count= count+1
    print("count=",count)
    averageEntropy=entropyData/count
    if(averageEntropy>6.667 ):
        return 1
    else:
        return 0


def encrypFile(clsdata):
    """ Calculated Encrypted text of the given clear text.
    """
    moo = AES.AESModeOfOperation()
    cypherkey = [143,194,34,208,145,203,230,143,177,246,97,206,145,92,255,84]
    iv = [103,35,148,239,76,213,47,118,255,222,123,176,106,134,98,92]
    mode, orig_len, ciph = moo.encrypt(clsdata, moo.modeOfOperation["CBC"],
                                       cypherkey, moo.aes.keySize["SIZE_128"], iv)
    encryptedData= bytearray(ciph)
    return encryptedData

def dump_info(filename):
    p=pefile.PE(filename)
    print("Address of Entry Point : ", hex(p.OPTIONAL_HEADER.AddressOfEntryPoint))
    number_of_section = p.FILE_HEADER.NumberOfSections
    print("Number of section : ", number_of_section)
    print("Section name", "VirtualAddress", "VirtualSize ","SizeOfRawData")
    for section in p.sections:
        print (section.Name.decode("UTF-8"),"\t", hex(section.VirtualAddress),"\t",hex(section.Misc_VirtualSize),"\t", hex(section.SizeOfRawData) )

    
def usage():
    print("""
        Command Usage:
        -h             :  help
        -f <filename>
              """)
    

def main(argv):
    """ Start of the program """
    
    if len(argv)==0:      ## check of the arguments
        print("\n Improper command format")
        usage()
        sys.exit()
        
    filename=''  
    flow = False
    dump = False
    try:
        opts,args=getopt.getopt(argv,"hf:d",["ifile=", "dump"])   
    except getopt.GetoptError:
        print("\n Improper command format")
        usage()
        sys.exit()
        
    ## to read the arguments
    for opt,arg in opts:
        if opt=="-h":
            usage()
            sys.exit()
        elif opt in ("-f","--ifile"):
            filename=arg
            flow = True
        elif opt in ("d","--dump"):
            dump=True
        else:
             print("\n Improper command format")
             usage()
             sys.exit()
    if flow :
        #print(filename)
        if os.path.isfile(filename):
            #print("File name  : ",filename)
            openfile = open(filename,'rb')
            readfile = openfile.read()
            print("Entropy of file is ", H(readfile))
       
            pe=pefile.PE(filename)
            sizeofHeader = pe.OPTIONAL_HEADER.SizeOfHeaders
            unknownEntropy = []
            unknownPackedEntropy = []
            for section in pe.sections:
                init=section.VirtualAddress
                last=section.VirtualAddress+section.Misc_VirtualSize
                sectionData= readfile[init:last]
                unknownEntropy.append(HsetReduction(sectionData))

                hex_bytes = binascii.hexlify(sectionData)
                cleartext = hex_bytes.decode("utf-8")
                cipherText= encrypFile(cleartext)
                unknownPackedEntropy.append(HsetReduction(cipherText))
            TotalunknownEntropy= 0
            TotalunknownPackedEntropy = 0 
            for i in range (len(unknownEntropy)):
                TotalunknownEntropy = TotalunknownEntropy+ unknownEntropy[i]
                TotalunknownPackedEntropy = TotalunknownPackedEntropy+ unknownPackedEntropy[i]
            firstEntropy = TotalunknownEntropy/len(unknownEntropy)
            secondEntropy =TotalunknownPackedEntropy/len(unknownPackedEntropy)
            #print("First Entropy = ",firstEntropy)
            #print("Entropy after packing = ",secondEntropy)
            TestingList = [firstEntropy,secondEntropy,(secondEntropy-firstEntropy)]
            predictedResult = KNN.ibk(TestingList)
            print(filename," is ",predictedResult)
            #KNN.ibktest()
            if dump:
                print(dump_info(filename))
        
        else:
            print("File doesn't exit or path is improper")
    else:
        print("\n Improper command format")
        usage()
    
if __name__ == "__main__":
    main(sys.argv[1:])
    
###End of the prgoram################################################################       
