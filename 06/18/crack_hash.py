#This script will require two inputs: the location of the wordlist and the hash value to be cracked. 
# It will then iterate through the wordlist, hashing each password and comparing it to the provided hash value. 
# If a match is found, it will print the password and exit.

import hashlib

wordlist_location = str(input('Enter wordlist file location: '))
hash_input = str(input('Enter hash to be cracked: '))

with open(wordlist_location, 'r') as file:
    for line in file.readlines():
        hash_ob = hashlib.md5(line.strip().encode())
        hashed_pass = hash_ob.hexdigest()
        if hashed_pass == hash_input:
            print('Found password! ' + line.strip())
            exit(0)