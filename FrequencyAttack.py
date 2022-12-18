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


from Crypto.Util.number import long_to_bytes

def main():
	f = open("text", "r")
	text = f.read()
	f.close()

	print( *[len(i) for i in text.split("\n")] )

	# alpha = [""]*27
	# k = 0

	# for letter in text:
	# 	if not(letter in alpha):
	# 		alpha[k] = letter
	# 		k += 1
	# print(k)

	# for i in range(len(alpha)):
	# 	for j in range(i+1, len(alpha)):
	# 		if text.count(alpha[i]) < text.count(alpha[j]):
	# 			alpha[i], alpha[j] = alpha[j], alpha[i]

	# summ = (len(text)-text.count(" "))
	# for word in alpha:
	# 	print(word, text.count(word)/summ*100)

	# row = " eoitsanhrldfmcwyugpbkv"
	# for i in range(len(row)):
	# 	text = text.replace(alpha[i], row[i])
	# print(text)



def grouper(iterable, n):
    args = [iter(iterable)] * n
    return zip(*args)


if __name__ == "__main__":
    main()
