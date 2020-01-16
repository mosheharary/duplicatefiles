import sys
import hashlib
from collections import defaultdict

def file_as_bytes(file):
    with file:
        return file.read()

def list_files_recursive(path):

    import os
    dd_md5 = defaultdict(list)
    dd_size = defaultdict(list)
    total_files=0


    for r, d, f in os.walk(path):
    #go over a directory - recursive
        for file in f:
            path=os.path.join(r, file)
            #get the full path of the file
            if os.path.isfile(path) == True:
            #check if it's a file
                size=os.path.getsize(path)
                #check size in bytes
                dd_size[size].append(path)
                #inset to hash - key is the size
                length=len(dd_size[size])
                total_files += 1
                if length > 1:
                    #if we have another file with the same size , caluculate its md5
                    tmp_file=dd_size[size].pop(0)
                    #we pop the first file from the hash (so we will not calculate it's md5 twice)
                    md5=hashlib.md5(file_as_bytes(open(tmp_file, 'rb'))).hexdigest()
                    dd_md5[md5].append(path)
                    #put the file in a diffrent hash when the key is the md5
                    if len(dd_md5[md5]) == 1:
                        #if , after the append , the size is 1 , we have to inset the first one also (the one that we pop)
                        dd_md5[md5].append(tmp_file)

#go over the md5 hash files and print the name(full path) of it
    print ("Scan " + str(total_files) + " files...")
    print ("duplicate files with the same md5:")
    for key,val in dd_md5.items():
        print ("md5:"+key)
        for file in dd_md5.get(key):
            print ("\t" + file)
        #print (dd_md5.get(key))


if __name__ == '__main__':

    for arg in sys.argv[1:]:
        print (arg + ":")
        list_files_recursive(arg)
