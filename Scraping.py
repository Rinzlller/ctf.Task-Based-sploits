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

import re

def main():
    f = open("strings", "r")
    file = f.read()
    f.close()
    
    strs = re.findall(r"db '(.*)',0", file)
    print(strs)


if __name__ == "__main__":
    main()
