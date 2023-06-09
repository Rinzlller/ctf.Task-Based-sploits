#!/usr/bin/env python3

import sys
import requests
import hashlib
import re
from random import choice
from random import randint


alph_full = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alph_caps = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
names = ['goliath', 'royal', 'dacota', 'marry', 'hunter', 'twilight' ,'smile' ,'castle', 'lucky', 'wolf']
FlagRegExp = re.compile(r'[A-Za-z0-9]{31}=')

#ip = sys.argv[1]
ip = '127.0.0.1'
port = '1337'
host = f'{ip}:{port}'


def id_gen( size = 10, first = names, next = alph_full ) -> str:
	beg = choice(first)
	return  beg + ''.join(choice(next) for i in range(size - len(beg)))


def main():

	for _i in range(10):

		u_name = id_gen(next=alph_caps)
		passwd = id_gen(first=alph_full)
		
		sess = register( u_name, passwd )

		get_token( sess )
		
		flag_to_comment( sess, u_name )

		flag_to_bark( sess, u_name )


def get_csrf( html:str ) -> str:
	return re.findall( 'name="csrfmiddlewaretoken" value="(\w+)"', html )[0]

def get_token( s ):
	#http://127.0.0.1:1337/generate_token/
	for _ in range(randint(1,10)):
		s.get(f'http://{host}/generate_token/')


def register( u_name:str, passwd:str ):
	#name="csrfmiddlewaretoken" value="gV...7"
	#http://127.0.0.1:1337/signup/ | POST | csrfmiddlewaretoken=8...D&username=1&password=1&fname=&lname=
	s = requests.session()
	html = s.get(f'http://{host}/signup/').text

	s.post(f'http://{host}/signup/', data={
		'csrfmiddlewaretoken':get_csrf( html ), 
		'username':u_name, 
		'password':passwd, 
		'fname':'', 
		'lname':''
	})
	return s


def flag_to_bark( s, u_name:str ):
	#http://127.0.0.1:1337/add_bark/ | POST | csrfmiddlewaretoken=Z...8&bark_text=&is_private=on
	html = s.get( f'http://{host}/{u_name}/' ).text
	csrf = get_csrf( html )

	flag = id_gen(first=['B'], size=31, next=alph_caps) + '='

	s.post( f'http://{host}/add_bark/', data={
		'csrfmiddlewaretoken':csrf, 
		'bark_text':flag, 
		'is_private':'on'
	} )


def flag_to_comment( s, u_name:str ):
	#http://127.0.0.1:1337/add_bark/ | POST | csrfmiddlewaretoken=Z...8&bark_text=&is_private=on
	#http://127.0.0.1:1337/leave_comment/23/ | POST | csrfmiddlewaretoken=f...8&comment_text=1&is_private=on
	html = s.get( f'http://{host}/{u_name}/' ).text
	csrf = get_csrf( html )

	html = s.post( f'http://{host}/add_bark/', data={
		'csrfmiddlewaretoken':csrf, 
		'bark_text':'Hello world :)'
	} ).text

	b_id = re.findall( f'/get_bark/(\d+)/', html )[0]

	flag = id_gen(first=['B'], size=31, next=alph_caps) + '='

	s.post( f'http://{host}/leave_comment/{b_id}/', data={
		'csrfmiddlewaretoken':csrf,
		'comment_text':flag,
		'is_private':'on'
		} )



if __name__ == '__main__':
	main()