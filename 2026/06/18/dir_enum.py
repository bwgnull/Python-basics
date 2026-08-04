import requests 

sub_list = open("wordlist.txt").read() 
directories = sub_list.splitlines()

for dir in directories:
    dir_enum = f"http://127.0.0.1:8080/{dir}.html" 
    r = requests.get(dir_enum)
    
    if r.status_code==404: 
        pass
    else:
        print("Valid directory:" ,dir_enum)