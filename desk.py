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

def main():
    v = [
    497, 1207, 1273, 871, 476, 884, 1615,
    475, 2233, 231, 505, 1919, 190, 2755,
    231, 561
    ]

    for i in range(0,len(v)//2):
        g = gcd(v[i*2], v[i*2+1])
        print(chr(g), end="")


if __name__ == "__main__":
    main()
