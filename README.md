# skEntropy

####Introduction
The name of the tool is skEntropy (ScanEntropy). This is designed to determine packed and not packed executable using entropy difference method
####Usage

skEntropy.py -f filename

skEntropy.py -h 

skentropy -f filename --dump



####Working

This tool take a file as input and  use [feature set-reduction method](http://ieeexplore.ieee.org/xpl/login.jsp?tp=&arnumber=6912767&url=http%3A%2F%2Fieeexplore.ieee.org%2Fiel7%2F6903647%2F6912720%2F06912767.pdf%3Farnumber%3D6912767) to calculate the entropy of the file. The file is encrypted using [AES algorithm](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) and entropy of the encrypted file is calculated. The difference in the first entropy and second entropy is calculated and all the three values (first entropy, second entropy and difference entropy) are given to the K-nearest neighbor algorithm [KNN/IBK]. KNN algorithm uses 869 known  [sample data](https://github.com/Kamlapati/skEntropy/tree/master/sample) to determine if excutable is packed and not packed. 

####Scope
Currently tool support PEexe files. 

####Additional resources

[PEfile](https://github.com/erocarrera/pefile). This module is used to navigate through the PE executable file. 
