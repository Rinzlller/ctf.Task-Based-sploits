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
port = '5002'
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
		
		add_flag( sess )


def register( u_name, passwd ):
	#http://127.0.0.1:5002/register | POST | login=name&type=1&password=pass
	requests.post(f'http://{host}/register', data = {'login':u_name, 'type':'1', 'password':passwd})


def login( u_name, passwd ):
	#http://127.0.0.1:5002/login | POST | login=name&password=pass
	s = requests.session()
	s.post(f'http://{host}/login', data = {'login':u_name, 'password':passwd})
	return s


def add_flag( s ):
	#http://127.0.0.1:5002/create | POST | name=text&text=flag
	flag = id_gen(first=['B'], size=31, next=alph_caps) + '='
	s.post( f'http://{host}/create', data={"name":"Some text", "text":flag} )


if __name__ == '__main__':
	main()