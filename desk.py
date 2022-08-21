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
	#f = open("strings", "r")
	file = '''
	In [1]: chr(0x4d)
	Out[1]: 'M'

	In [2]: chr(0x75)
	Out[2]: 'u'

	In [3]: chr(0x74)
	Out[3]: 't'

	In [4]: chr(0x34)
	Out[4]: '4'

	In [5]: chr(0x64)
	Out[5]: 'd'

	In [6]: chr(0x33)
	Out[6]: '3'

	In [7]: chr(0x64)
	Out[7]: 'd'

	In [8]: chr(0x5F)
	Out[8]: '_'

	In [9]: chr(0x43)
	Out[9]: 'C'

	In [10]: chr(0x75)
	Out[10]: 'u'

	In [11]: chr(0x63)
	Out[11]: 'c'

	In [12]: chr(0x75)
	Out[12]: 'u'

	In [13]: chr(0x6D)
	Out[13]: 'm'

	In [14]: chr(0x62)
	Out[14]: 'b'

	In [15]: chr(0x33)
	Out[15]: '3'

	In [16]: chr(0x72)
	Out[16]: 'r'

	In [17]: chr(0x73)
	Out[17]: 's'

	In [18]: chr(0x5f)
	Out[18]: '_'

	In [19]: chr(0x6b)
	Out[19]: 'k'

	In [20]: chr(0x31)
	Out[20]: '1'

	In [21]: chr(0x6c)
	Out[21]: 'l'

	In [22]: chr(0x6c)
	Out[22]: 'l'

	In [23]: chr(0x5f)
	Out[23]: '_'

	In [24]: chr(0x55)
	Out[24]: 'U'

	In [25]: chr(0x6e)
	Out[25]: 'n'

	In [26]: chr(0x31)
	Out[26]: '1'

	In [27]: chr(0x63)
	Out[27]: 'c'

	In [28]: chr(0x6f)
	Out[28]: 'o'

	In [29]: chr(0x72)
	Out[29]: 'r'

	In [30]: chr(0x6e)
	Out[30]: 'n'

	In [31]: chr(0x35)
	Out[31]: '5'
	'''#f.read()
	#f.close()

	# for str in file.split("malloc(20)"):
	flag = re.findall(r"]: '(.*)'", file)
	print("".join(flag))


if __name__ == "__main__":
    main()
