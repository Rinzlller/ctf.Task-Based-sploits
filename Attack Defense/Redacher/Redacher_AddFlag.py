#!/usr/bin/env python3

import sys
import requests
import hashlib
import re
from random import choice


alph_full = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alph_caps = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
names = ['goliath', 'royal', 'dacota', 'marry', 'hunter', 'twilight' ,'smile' ,'castle', 'lucky', 'wolf']
FlagRegExp = re.compile(r'[A-Za-z0-9]{31}=')

#ip = sys.argv[1]
ip = '127.0.0.1'
port = '5000'
host = f'{ip}:{port}'


def id_gen( size = 10, first = names, next = alph_full ):
	beg = choice(first)
	return  beg + ''.join(choice(next) for i in range(size - len(beg)))


def main():

	for _i in range(40):

		u_name = id_gen(next=alph_caps)
		passwd = id_gen(first=alph_full)
		
		register( u_name, passwd )
		sess = login( u_name, passwd )
		
		add_flag( sess, new_thread_id(sess) )


def register( u_name, passwd ):
	#http://127.0.0.1:5000/register | POST | login=name&password=pass
	requests.post(f'http://{host}/register', data = {'login':u_name, 'password':passwd})


def login( u_name, passwd ):
	#http://127.0.0.1:5000/login | POST | login=name&password=pass
	s = requests.session()
	s.post(f'http://{host}/login', data = {'login':u_name, 'password':passwd})
	return s


def new_thread_id( s ):
	#http://127.0.0.1:5000/create | POST | name=Name
	data = s.post(f'http://{host}/create', data={"name":"SuperNews"}).text
	return  re.findall( "/threads/(\d+)", data )[0]


def add_flag( s, t_id ):
	#http://127.0.0.1:5000/threads/5 | POST | text=flag
	flag = id_gen(first=['R'], size=31, next=alph_caps) + '='
	s.post( f'http://{host}/threads/{t_id}', data={"text":flag} )


if __name__ == '__main__':
	main()