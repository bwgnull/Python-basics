#This file is used to download a file from a remote server. The code sends a GET request to the specified URL and saves the content of the response to a local file named by the user. 
#The user is prompted to enter the URL of the file to download and the name of the file to save as. 
#The code uses the requests library to send the GET request and handle the response.

import requests

url = input('Enter the URL of the file to download: ')
r = requests.get(url, allow_redirects=True)
filename = input('Enter the name of the file to save as: ')
open(filename, 'wb').write(r.content)  