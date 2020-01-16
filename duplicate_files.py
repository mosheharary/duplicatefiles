import sys
import hashlib
from collections import defaultdict

def calc_hash(file,check_all):

    BLOCK_SIZE = 65536

    file_hash = hashlib.sha256()
    with open(file, 'rb') as f:
        fb = f.read(BLOCK_SIZE)
        if check_all == False:
            file_hash.update(fb)
            return file_hash.hexdigest()
            #only check calculate the first block of the file
        while len(fb) > 0:
            file_hash.update(fb)
            fb = f.read(BLOCK_SIZE)

    return file_hash.hexdigest()

def list_files_recursive(path):

    import os
    import stat
    dd_hash = defaultdict(list)
    dd_hash_part = defaultdict(list)
    dd_size = defaultdict(list)
    total_files=0


    for r, d, f in os.walk(path):
    #go over a directory - recursive
        for file in f:
            path=os.path.join(r, file)
            #get the full path of the file
            if os.access(path, os.R_OK) == False:
                print ("Can not read " + path)
                continue
            if os.path.isfile(path) == True:
            #check if it's a file
                st = os.stat(path)
                size=st.st_size
                #get size in bytes
                dd_size[size].append(path)
                #inset to hash , key is the size
                total_files += 1

    for key,val in dd_size.items():
        if len(val) > 1:
        #check if we have an entry > 1 in size based hash
            for file in dd_size.get(key):
                hash=calc_hash(file,False)
                #calculate file hash based on the first file block only and inset to another hash
                dd_hash_part[hash].append(file)

    for key,val in dd_hash_part.items():
        if len(val) > 1:
        #check if we have an entry > 1 in partial file  based hash
            for file in dd_hash_part.get(key):
                hash=calc_hash(file,True)
                #calculate file hash and inset to another hash
                dd_hash[hash].append(file)

    print ("Scan " + str(total_files) + " files...")
    print ("duplicate files with the same hash:")
    for key,val in dd_hash.items():
        if len(val) > 1:
        #print only hash entries > 1
            print ("hash:"+key)
            for file in dd_hash.get(key):
                print ("\t" + file)




if __name__ == '__main__':

    for arg in sys.argv[1:]:
        print (arg + ":")
        list_files_recursive(arg)