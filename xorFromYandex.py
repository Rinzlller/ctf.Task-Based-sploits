#!/usr/bin/env python3

# WORDLIST:	/usr/share/wordlists/rockyou.txt

# from urllib.parse import quote, unquote			#unquote("%2F")		quote("\")
# from html import unescape
# from hashlib import md5

# from pwn import *
# from os import system

# import string

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

import requests
from base64 import *
from json import dumps, loads							#dumps({"key":"value"})

host = "https://cgcookie.shkib.space/index"

def main():

	cookie_b64 = "eyJpdiI6IjVCY2lnaDhDdGw2dzc5dTVVMGI2L1E9PSIsIm5vbmNlIjoiTjVGSWRPanRPTGlYMzhYMWhTVXlCUT09IiwicGF5bG9hZCI6IlVPdlNsYXJrWDhIYit3SWRYZDVpZHo4QkJnaEFqZ29wL1JMZGRHWHhZMkE9In0="
	cookie = loads( b64decode(cookie_b64).decode() ) 

	iv = b64decode(cookie["iv"])
	nonce = b64decode(cookie["nonce"])
	payload = b64decode(cookie["payload"])

	payload = b'P\xeb\xd2\x95\xaa\xe4_\xc1\xdb\xfb\x02\x1d]\xdebw?\x01\x06\x08@\x8e\n)\xfd\x12\xddte\xf1c`'
	nonce = b'7\x91Ht\xe8\xed8\xb8\x97\xdf\xc5\xf5\x85%2\x05'
	iv = b'\xe4\x17"\x82\x1f\x02\xb6^\xb0\xef\xdb\xbc\x17G\xfd\xb9'

	# payload = payload[:16]
	# nonce = payload
	# iv = b"{\"user_id\"=2827}"

	# {'user_id'=28278 1...

	cookie = {
		"iv": b64encode(iv).decode(),
		"nonce": b64encode(nonce).decode(),
		"payload": b64encode(payload).decode()
	}
	cookie_b64 = b64encode(dumps(cookie).encode()).decode()

	s = requests.Session()
	resp = s.get(host, cookies = {"SessionID": cookie_b64}, allow_redirects=False)
	print(resp.text)


if __name__ == "__main__":
	main()
