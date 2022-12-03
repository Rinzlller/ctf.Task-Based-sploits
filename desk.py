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

# <-->
# <-<

# -><
# ->-

def main():

	a = 102078
	b = 42019
	p = 103837

	for i in range(1000000):
		if pow(a, i, p)==b:
			print(i)
			break


if __name__ == "__main__":
    main()
